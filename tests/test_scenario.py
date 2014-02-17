"""
Scenario for Product
"""
from datetime import datetime
from datetime import timedelta

from unittest import TestCase

from zuora.client import Zuora


class FullScenarioTestCase(TestCase):

    def setUp(self):
        self.client = Zuora()

    def create_catalog(self):
        now = datetime.now()
        one_year = datetime.now() + timedelta(days=365)

        self.client = Zuora()
        p = self.client.instanciate('Product')
        p.Name = 'Test subscription'
        p.EffectiveStartDate = now
        p.EffectiveEndDate = one_year
        p_response = self.client.create(p)
        self.assertEquals(p_response[0].Success, True)
        product_id = p_response[0].Id
        self.product_id = product_id

        product_rate_plans = []
        for name in ('Silver', 'Gold', 'Diamond'):
            prp = self.client.instanciate('ProductRatePlan')
            prp.Name = name
            prp.ProductId = product_id
            prp.EffectiveStartDate = now
            prp.EffectiveEndDate = one_year
            # Custom fields
            prp.ZZ00_referencenumber__c = 'test'
            prp.ZZ01_MinimumDuration__c = '1'  # Not mandatory
            prp.ZZ02_VisiblePortal__c = 'yes'
            prp.ZZ03_CanGenerateaForm__c = 'no'
            # End custom fields
            product_rate_plans.append(prp)

        product_rate_plan_response = self.client.create(product_rate_plans)
        prp_ids = [prp.Id for prp in product_rate_plan_response]
        prp_successes = [prp.Success for prp in product_rate_plan_response]
        self.assertEquals(prp_successes, [True, True, True])

        product_rate_plan_pricings = []
        for i, prp_id in enumerate(prp_ids):
            prpc = self.client.instanciate('ProductRatePlanCharge')
            prpc.Name = 'Recurring Flat fee'
            prpc.BillCycleType = 'DefaultFromCustomer'
            prpc.BillingPeriod = 'Month'
            prpc.ChargeModel = 'Flat Fee Pricing'
            prpc.ChargeType = 'Recurring'
            prpc.ProductRatePlanId = prp_id
            prpc.TriggerEvent = 'ContractEffective'
            prpct = self.client.instanciate('ProductRatePlanChargeTier')
            prpct.Currency = 'EUR'
            prpct.Price = 30 - (i * 2.5)
            prpc.ProductRatePlanChargeTierData.ProductRatePlanChargeTier = [
                prpct]
            product_rate_plan_pricings.append(prpc)
        product_rate_plan_pricing_response = self.client.create(
            product_rate_plan_pricings)
        prpc_successes = [prpc.Success for prpc in
                          product_rate_plan_pricing_response]
        self.assertEquals(prpc_successes, [True, True, True])

    def delete_catalog(self):
        delete_response = self.client.delete('Product', self.product_id)

    def test_scenario(self):
        self.create_catalog()
        self.delete_catalog()
