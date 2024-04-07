import json
from math import exp

# takeing inputs
class auxi_func():        
    
    def __init__(self, plane: str, cruise_range: list[float], endurance: list[float], n_souls: int, fixed_payload: float, dropable_payload: int = 0, dp = 2) -> None:
        # Initial Set up
        self.plane: str = plane   # plane type: jet transport (jt), figher jet (jt), and sailplane (sp)

        # Loading our json file to set plane constants. 
        with open("AVD_constants.json") as fh_read:
            data = json.load(fh_read)

        # Loading aircraft constants
        if self.plane == "jt": self.const: dict = data["jet transport"] 
        elif self.plane == "fj": self.const: dict = data["fighter jet"]
        elif self.plane == "sp": self.const: dict = data["seaplane"]
        else: print("No aircraft has been selected.")
        
        # loading universal constants
        self.uni_const = data["uni_constants"]
        
        # Secondary Setup
        self.payload: float = sum([n_souls*self.uni_const["souls_weight"], fixed_payload, dropable_payload])
        self.cruise_range = cruise_range if type(cruise_range) == list else [cruise_range]
        self.endurance = endurance if type(endurance) == list else [endurance]
        self.dp = dp

    # def payloads(self) -> float:
    #     return sum(n_souls*auxi_func.uni_constants["uni_constants"], fixed_payload, dropable_payload)

    def calc_We_W0(self, W0_guess: float = 2267.962, refine = False) -> float:
        if refine:
            """
            Returns the refined calculations of the empty weight fractions given an assumed take-off weight, W0_guess."""
            Kvc = self.const["Kvc"]
            a = self.const["a"]
            b = self.const["b"]
            C1 = self.const["C1"]
            C2 = self.const["C2"]
            C3 = self.const["C3"]
            C4 = self.const["C4"]
            C5 = self.const["C5"]
            A = self.const["A"]
            T_W = self.calc_T_W()
            W_S = self.calc_W_S()
            M = self.const["M"][0]

            # Calculating 
            self.We_W0 = round( (a + (b * (W0_guess**C1) * (A**C2) * (T_W**C3) * (W_S**C4) * (M**C5))) * Kvc, self.dp)
        
        else:
            A = self.const["A"]
            c = self.const["c"]
            Kvc = self.const["Kvc"]
            """
            Returns the crude calculations of the empty weight fractions given an assumed take-off weight, W0_guess."""
            self.We_W0 = round(A * W0_guess **(c) * Kvc, self.dp)
        
        return self.We_W0

    # def refined_We_W0(self, W0_guess: float = 2267.962) -> float:

    def calc_T_W(self) -> float:
        N = self.uni_const["N_engines"]
        L_D = self.const["L_D"]
        Y_sscg = self.uni_const["Y_sscg"]
        Y_ma = self.uni_const["Y_ma"]

        self.T_W = round( max((N/(N-1)) * ((L_D)**(-1)+Y_sscg), (N/(N-1)) * ((L_D)**(-1)+Y_ma)), self.dp)
        return self.T_W
    
    def calc_W_S(self) -> float:
        rho = self.uni_const["air_density"]
        Cl_max = self.uni_const["Cl_max"]
        V = self.const["M"][0] * self.uni_const["V_sound"]

        # print(0.5 * rho * (V**2) * Cl_max)
        self.W_S = round( 0.5 * rho * (V**2) * Cl_max, self.dp )
        return self.W_S
    
    def calc_Wf_W0(self) -> float:
        acc = True if self.plane == "fj" else False
        rff = self.const["allowance"]
        Wi_W0 = self.calc_W_fraction(acc)
        
        # returns the weight fraction on an unaccelerated climb (crude method)
        self.Wf_W0 = round( (1+rff)*(1-Wi_W0), self.dp)
        return self.Wf_W0
    
    def calc_Wf(self, W0_guess, refine = False) -> None:
        W0_guess = self.uni_const["W0_guess"] if bool(W0_guess) else W0_guess
        W_fuel = 0
        if refine:
            for i in self.const["W_fraction"]:
                try:
                    W_fuel = (1 - i[0])*W0_guess
                    W0_guess = W0_guess - W_fuel

                except TypeError:
                    if i[0] == "c":
                        i = self.range_eqn()
                    elif i[0] == "l":
                        i = self.endurance_eqn()
                    else:
                        print("Check your AVD_constants.")

                    W_fuel = (1 - i)*W0_guess
                    W0_guess = W0_guess - W_fuel

        else:
            for i in self.const["W_fraction"]:
                try:
                    W_fuel = (1 - self.acc_climb())*W0_guess if i[1] else (1 - i[0]) * W0_guess
                        
                except TypeError:
                    if i[0] == "c":
                        i = self.range_eqn()
                    elif i[0] == "l":
                        i = self.endurance_eqn()
                    else:
                        print("Check your constants.")
                        exit()
                    
                    W_fuel = (1 - i)*W0_guess
                    W0_guess = W0_guess - W_fuel

        self.payload = self.payload + W_fuel

    def calc_W_fraction(self, refine = False, status = 0) -> float:
        if bool(status): return 0
        # computing the weight fractions as needed.
        result = 1.0
        if not refine:
            for i in self.const["W_fraction"]:
                try:
                    result = result * i[0]
                except TypeError:
                    if i[0] == "c":
                        i = self.range_eqn()
                    elif i[0] == "l":
                        i = self.endurance_eqn()
                    else:
                        print("Check your AVD_constants.")
                    
                    result = result * i
        else:
            for i in self.const["W_fraction"]:
                try:
                    result = result * self.acc_climb() if i[1] else result * i[0]    # I need to check this
                        
                except TypeError:
                    if i[0] == "c":
                        i = self.range_eqn()
                    elif i[0] == "l":
                        i = self.endurance_eqn()
                    else:
                        print("Check your AVD_constants.")
                        exit()
                    
                    result = result * i
        self.W_fraction = result
        return self.W_fraction

    def acc_climb(self) -> float:
        # Constants Setup
        result = 1
        for M in self.const["M"]:
            # Calculating for either subsonic accelerated climb or supersonic accelerated climb
            W = (0.991 - 0.007*M - 0.01*M**2) if M >= 1.0 else (1.0065 - 0.0325*M)
            result = W/result

        return round(result, self.dp)

    def range_eqn(self) -> float:
        # Values setup
        result = 1
        R = self.cruise_range
        Csp = self.const["Csp_cruise"]
        V = min(self.const["M"]) * self.uni_const["V_sound"]
        L_D = self.const["L_D"]

        # computing the product of the ranges of cruise
        for r in R: result = exp(-(r*Csp)/(V*L_D)) * result

        # returning our results
        return round(result, self.dp)

    def endurance_eqn(self) -> float:
        # Values setup
        result = 1
        E = self.endurance
        Csp = self.const["Csp_loiter"]
        L_D = self.const["L_D"]

        # computing the product of the ranges of cruise
        for e in E: result = exp(-(e*Csp)/(L_D)) * result

        # returning our results
        return round(result, self.dp)
    
    def __main(self, x=4000) -> float:
        W = round(self.payload/(1-self.calc_We_W0() - self.calc_Wf_W0()), self.dp) 
        return {"Weight": W}


if __name__ == "__main__":
    # print(dir(auxi_func))
    plane = input("Select a plane type:\njt for Jet Transport\nfj for Fighter jet\nsp for seaplane\n>> ")
    cruise_range = float(input("Enter your cruise range: "))
    endurance = float(input("Enter the endurance: "))
    n_souls = int(input("Enter the number of individuals to board the airplane: "))
    payload = float(input("Enter the payload you are to carry: "))
    y = auxi_func(plane, cruise_range, endurance, n_souls, payload)  # plane: str, cruise_range: list[float], endurance: list[float], n_souls: int, fixed_payload: float, dropable_payload: int = 0, dp = 2
    
    print(y.main())