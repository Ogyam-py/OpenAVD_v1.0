import json
# takeing inputs
class auxi_func():        
    
    def __init__(self, plane: str, n_souls: int, fixed_payload: float, dropable_payload: int = 0) -> None:
        # Initial Set up
        self.plane: str = plane   # plane type: jet transport (jt), figher jet (jt), and sailplane (sp)

        # Loading our json file to set plane constants. 
        with open("AVD_constants.json") as fh_read:
            data = json.load(fh_read)

        # Loading aircraft constants
        self.const = data["jet transport"] if self.plane == "jt" else data["fighter jet"]
        if self.const == "sp": self.const = data["seaplane"]
        
        # loading universal constants
        self.uni_const = data["uni_constants"]
        
        # Secondary Setup
        self.payload: float = sum([n_souls*self.uni_const["souls_weight"], fixed_payload, dropable_payload])


    # def payloads(self) -> float:
    #     return sum(n_souls*auxi_func.uni_constants["uni_constants"], fixed_payload, dropable_payload)

    def crude_We_W0(self, W0_guess: float = 2267.962) -> float:
        A = self.const["A"]
        c = self.const["c"]
        Kvc = self.const["Kvc"]
        """
        Returns the crude calculations of the empty weight fractions given an assumed take-off weight, W0_guess."""
        return A * W0_guess **(c) * Kvc
    
    def refined_We_W0(self, W0_guess: float = 2267.962) -> float:
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
        M = self.const["M"]

        return (a + (b * (W0_guess**C1) * (A**C2) * (T_W**C3) * (W_S**C4) * (M**C5))) * Kvc

    def calc_T_W(self) -> float:
        N = self.uni_const["N_engines"]
        L_D = self.const["L_D"]
        Y_sscg = self.uni_const["Y_sscg"]
        Y_ma = self.uni_const["Y_mg"]

        return max((N/(N-1)) * ((L_D)**(-1)+Y_sscg), (N/(N-1)) * ((L_D)**(-1)+Y_ma))
    
    def calc_W_S(self) -> float:
        rho = self.uni_const["air_density"]
        Cl_max = self.uni_const["Cl_max"]
        V = self.const["M"] * self.uni_const("V_sound")

        return 0.5 * rho * (V**2) * Cl_max
    
    def main(self, x=4000):
        return auxi_func.crude_We_W0(x)


if __name__ == "__main__":
    print(dir(auxi_func))
    y = auxi_func("fj", 200, 200, 100)
    print(y.main())

