import biosteam as bst

class TEA(bst.TEA):
    """
    Create a TEA object for techno-economic analysis of a biorefinery.
    """

    __slots__ = ('labor_cost', 'fringe_benefits', 'maintenance',
                 'property_tax', 'property_insurance', '_FCI_cached',
                 'supplies', 'maintanance', 'administration', 'equipment')

    def __init__(self, system, IRR, duration, depreciation, income_tax,
                 operating_days, lang_factor, construction_schedule, WC_over_FCI,
                 labor_cost, fringe_benefits, property_tax,
                 property_insurance, supplies, maintenance, administration, equipment):
        super().__init__(system, IRR, duration, depreciation, income_tax,
                         operating_days, lang_factor, construction_schedule,
                         startup_months=0, startup_FOCfrac=0, startup_VOCfrac=0,
                         startup_salesfrac=0, finance_interest=0, finance_years=0,
                         finance_fraction=0, WC_over_FCI=WC_over_FCI)
        self.labor_cost = labor_cost
        self.fringe_benefits = fringe_benefits
        self.property_tax = property_tax
        self.property_insurance = property_insurance
        self.supplies= supplies
        self.maintenance = maintenance
        self.administration = administration
        self.equipment = equipment

    def _other_supplies(self):
        other = {
            "Cooling Tower Chemicals": 0,
            "Catalyst": 0 # 9.75*344*8400*200/2000
        }

    def _DPI(self, installed_equipment_cost):
        # self.equipment = [["Metering bin", 150000.00],
        #             ["OCC Screen", 175000.00],
        #             ["Debris Roll Screen", 220000.00],
        #             ["News paper Screen", 400000.00],
        #             ["Polishing screen", 280000.00],
        #             ["Recycling Magnets", 35000.00],
        #             ["Eddy Current separator", 128000.00],
        #             ["Optical Plastic sorting machine ", 225000.00],
        #             ["Baler ", 550000.00],
        #             ["Conveyor", 50000.00],
        #             ["Rolling Stock", 350000.00],
        #             ["Collection Cars", 1000000.00]]

        total_costs = sum(self.equipment[i][1] for i in range(len(self.equipment)))*(self.system.flowsheet('Waste').get_total_flow('tonnes/hr')/30)**0.7

        # other_costs = [["Land",	675000.00],
        #             ["Site Work", 	720000.00],
        #             ["Scale House", 	600000.00],
        #             ["MRF Building",	8600000.00],
        #             ["Construction, planning & surveying",	3500000.00]]
        # total_costs = sum(self.other_costs[i][1] for i in range(len(other_costs)))*(self.system.flowsheet('Waste').get_total_flow('tonnes/hr')/30)**0.7 + total_equipment

        return total_costs

    def _TDC(self, DPI):
        return DPI

    def _FCI(self, TDC):
        self._FCI_cached = TDC
        return TDC

    # def show_graph(self):
    #     return

    def _FOC(self, FCI):
        return (FCI*(self.property_tax + self.maintenance)
                + self.labor_cost*(1+self.fringe_benefits+self.supplies+ self.administration) )