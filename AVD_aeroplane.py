from AVD_functions import auxi_func

# Creating a class to serve as a template for aircraft calculations.
class aeroplane(auxi_func):
    def __init__(self, plane: str, cruise_range: list[float], endurance: list[float], n_souls: int, fixed_payload: float, dropable_payload: int = 0, dp=2) -> None:
        super().__init__(plane, cruise_range, endurance, n_souls, fixed_payload, dropable_payload, dp)       

    # def crude_weight(self) -> int:
    #     # self.weight = 
    #     return round( self.payload()/(1 - self.calc_Wf_W0() - self.calc_We_W0()), self.dp)

    # def refined_weight(self) -> int:
    #     # self.weight = 
    #     return round( self.payload()/(1 - self.calc_We_W0(self.crude_weight(), True) ), self.dp)

    def takeoff_weight(self, refine = False):
        W0_guess = self.uni_const["W0_guess"]

        while True:
            self.weight = self.payload/(1 - self.calc_Wf_W0() - self.calc_We_W0())
            if abs(self.weight - W0_guess) <= (1/(10**self.dp)):
                break
            else:
                W0_guess = 0.5*(self.weight + W0_guess)
        
        if refine:
            W0_guess = self.weight
            self.calc_Wf(W0_guess, refine=True)   # adds the fuel weight to the payload weight
            while True:
                self.weight = round(self.payload/(1 - self.calc_We_W0(W0_guess, True)), self.dp)
                if abs(self.weight - W0_guess) <= (1/(10**self.dp)):
                    break
                else:
                    W0_guess = 0.5*(self.weight + W0_guess)
        return round(self.weight, self.dp)


    def engine_size(self) -> float:
        return round( self.weight * self.calc_T_W(), self.dp)
    
    def wing_size(self) -> float:
        # returns the length and Area of the wing, respectively.
        return (round((self.const["AR"]*(self.calc_W_S()**(-1)) * self.weight)**(0.5), self.dp), round(self.weight * self.calc_W_S()**-1, self.dp))

    def fuselage_sizing(self) -> float:
        # rtturns the length and diameter of the fuselage, respectively.
        return (round(self.wing_size()[0]*0.75, self.dp), round(self.wing_size()[0]*0.75*0.1, self.dp))
    
    def V_max(self):
        return round(max(self.const["M"]) * self.uni_const["V_sound"], self.dp)

    def RTD_cost(self, refine):
        We = self.We_W0 * self.weight # empty weight.
        V = 1.94384449 * self.V_max()  # Maximum veleocity in knots. Scale factor 1 m/s : 1.94384449 knots.
        Q = self.uni_const["Q"]  # Quantity produced.
        FTA = self.uni_const["FTA"] # Number of flight tests.
        N_eng = Q * self.uni_const["N_engines"] # Number of engines. Thus number of engines for the total aircraft production.
        T_max = 0.224809*self.engine_size() # Maximum thrust converted to lbf using the scale factor of 1N : 0.224809-lbf.
        M_max = max(self.const["M"]) # Maximum mach number.
        T_inlet = self.uni_const["T_inlet"] # Turbine inlet temperature (rankine).
        C_avionics = self.const["C_avionics"] # We excludethe cost of avionics. C_avionics = 0
        R_eng = self.uni_const["R_eng"]
        R_tooling = self.uni_const["R_tooling"]
        R_quality = self.uni_const["R_quality"]
        R_mfg = self.uni_const["R_mfg"]

        # Sub-calculations
        H_eng = 4.86*(We**0.777)*(V**0.894)*(Q**0.163)
        H_tooling = 5.99*(We**0.777)*(V**0.696)*(Q**0.263)
        H_mfg = 7.37*(We**0.82)*(V**0.484)*(Q**0.641)
        H_quality = 0.133*H_mfg
        C_d = 45.42*(We**0.63)*(V**1.3)
        C_f = 1243.03*(We**0.325)*(V*0.822)*(FTA**1.21)
        C_m = 11.0*(We**0.921)*(V**0.621)*(Q**0.799)
        C_eng = 1548*(0.043*T_max + 243.25*M_max + 0.969*T_inlet - 2228)

        return round(H_eng*R_eng + H_tooling*R_tooling + H_mfg*R_mfg + H_quality*R_quality + C_d + C_f + C_eng*N_eng + C_m + C_avionics, self.dp)

        

        return 101000
    
    def main(self, refine: bool):
        # The weight of the aircraft is to be calculated first before any thing else.
        return { 
            "weight": self.takeoff_weight(refine),
            "fuselage": str(self.fuselage_sizing()[0]) + '" ' + str(self.fuselage_sizing()[1]) + "'",
            "wing_size": str(self.wing_size()[0]) + '" ' + str(self.wing_size()[1]) + "'",
            "engine_size": self.engine_size(),
            "V_max": self.V_max(),
            "RTD&E": self.RTD_cost(refine)
            }

if __name__ == "__main__":
    # plane = input("Select a plane type:\njt for Jet Transport\nfj for Fighter jet\nsp for seaplane\n>> ")
    # cruise_range = float(input("Enter your cruise range: "))
    # endurance = float(input("Enter the endurance: "))
    # n_souls = int(input("Enter the number of individuals to board the airplane: "))
    # payload = float(input("Enter the payload you are to carry: "))
    # y = aeroplane(plane, cruise_range, endurance, n_souls, payload)  # plane: str, cruise_range: list[float], endurance: list[float], n_souls: int, fixed_payload: float, dropable_payload: int = 0, dp = 2
    
    y = aeroplane("sp", 1000, 900, 100, 10000, 100)
    print(y.main(True))
