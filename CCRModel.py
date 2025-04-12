import cvxpy as cp
import numpy as np
class CCR_Model:
    def __init__(self, X, Y):
        self.inputs = X
        self.outputs = Y
        self.dmus_number = X.shape[0]
        self.inputs_number = X.shape[1]
        self.outputs_number = Y.shape[1]

    def basic_calculate_theta(self, dmu_index):
        x0 = self.inputs[dmu_index]
        y0 = self.outputs[dmu_index]
        lambd = cp.Variable(self.dmus_number, nonneg=True)
        theta = cp.Variable()

        constraints = [
            (self.inputs).T @ lambd <= theta * x0,
            (self.outputs).T @ lambd >= y0
        ]

        prob = cp.Problem(cp.Minimize(theta), constraints)
        prob.solve()

        return theta.value, lambd.value

    def basic_rank_dmus(self):
        theta_values = []
        for i in range(self.dmus_number):
            theta = self.basic_calculate_theta(i)[0]
            theta_values.append(theta)
        return theta_values
    
    def slack_calculate_theta(self, dmu_index, epsilon=1e-6):
        x0 = self.inputs[dmu_index]
        y0 = self.outputs[dmu_index]
        lambd = cp.Variable(self.dmus_number, nonneg=True)
        theta = cp.Variable()
        s_minus = cp.Variable(self.inputs_number, nonneg=True)
        s_plus = cp.Variable(self.outputs_number, nonneg=True)

        constraints = [
        (self.inputs).T @ lambd + s_minus == theta * x0,
        (self.outputs).T @ lambd - s_plus == y0
        ]

        
        prob = cp.Problem(cp.Minimize(theta + epsilon * (cp.sum(s_minus) + cp.sum(s_plus))), constraints)
        prob.solve()

        return theta.value, s_minus.value, s_plus.value, lambd.value
    
    def slack_rank_dmus(self):
        theta_values = []
        for i in range(self.dmus_number):
            theta = self.slack_calculate_theta(i)[0]
            theta_values.append(theta)
        return theta_values
    
    def super_caculate_theta(self, dmu_index):
        x0 = self.inputs[dmu_index]
        y0 = self.outputs[dmu_index]
        lambd = cp.Variable(self.dmus_number - 1, nonneg=True)
        theta = cp.Variable()
        inputs_excl = np.delete(self.inputs, dmu_index, axis=0)
        outputs_excl = np.delete(self.outputs, dmu_index, axis=0)

        constraints = [
        inputs_excl.T @ lambd <= theta * x0,
        outputs_excl.T @ lambd >= y0
        ]

        prob = cp.Problem(cp.Minimize(theta), constraints)
        prob.solve()

        return theta.value, lambd.value
    
    def super_rank_dmus(self):
        theta_values = []
        for i in range(self.dmus_number):
            theta = self.super_caculate_theta(i)[0]
            theta_values.append(theta)
        return theta_values






if __name__ == '__main__':
    X = np.array([[6, 2], [82, 4], [1004, 1000]])  # inputs (n x m)
    Y = np.array([[5], [4], [300000]])          # outputs (n x s)

    model = CCR_Model(X, Y)
    print(model.basic_rank_dmus())
    print()
    print(model.slack_rank_dmus())
    print()
    print(model.super_rank_dmus())
