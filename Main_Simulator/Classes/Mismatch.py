import numpy as np
import pandas as pd
import cmath

# --- Step 1: Known Power Values (MW and MVar) ---
S_base = 100  # MVA

# Bus ordering: 1 to 7
P_spec_MW = {
    1: 0,
    2: 0,
    3: -110,
    4: -100,
    5: -100,
    6: 0,
    7: 200
}

Q_spec_MVar = {
    1: 0,
    2: 0,
    3: -50,
    4: -70,
    5: -65,
    6: 0,
    7: 0
}

# --- Step 2: Convert to per unit ---
P_pu = [P_spec_MW[bus] / S_base for bus in range(1, 8)]
Q_pu = [Q_spec_MVar[bus] / S_base for bus in range(1, 8)]
y_pu = np.array(P_pu + Q_pu)

# --- Step 3: Flat Start Voltage (magnitude = 1.0, angle = 0) ---
V = np.ones(7)
delta = np.zeros(7)  # radians

# --- Step 4: Ybus matrix (7x7) ---
Ybus = np.array([
    [1.46329 - 14.63290j, -1.46329 + 14.63290j, 0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j],
    [-1.46329 + 14.63290j, 37.77746 - 127.05052j, -10.375479 + 32.137885j, -25.938697 + 80.344712j, 0 + 0j, 0 + 0j, 0 + 0j],
    [0 + 0j, -10.375479 + 32.137885j, -72.226879 + 104.062j, 0 + 0j, -12.969349 + 40.172365j, 0 + 0j, 0 + 0j],
    [0 + 0j, -25.938697 + 80.344712j, 0 + 0j, 46.319102 - 143.352043j, -7.411056 + 22.955632j, -12.969349 + 40.172365j, 0 + 0j],
    [0 + 0j, 0 + 0j, -12.969349 + 40.172365j, -7.411056 + 22.955632j, -25.938697 + 80.344712j, 46.319102 - 143.352043j, 0 + 0j],
    [0 + 0j, 0 + 0j, 0 + 0j, -12.969349 + 40.172365j, 40.489864 - 139.443204j, -25.938697 + 80.344712j, -1.581819 + 18.981824j],
    [0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j, -1.581819 + 18.981824j, 1.581819 - 18.981824j]
])

# --- Step 5: Compute yx using power flow equations ---
P_yx = []
Q_yx = []

for k in range(7):
    Pk = 0
    Qk = 0
    for n in range(7):
        Ykn = Ybus[k, n]
        Y_mag = abs(Ykn)
        theta_kn = cmath.phase(Ykn)
        angle_diff = delta[n] - delta[k]  # zero for flat start
        Pk += V[k] * V[n] * Y_mag * np.cos(theta_kn + angle_diff)
        Qk += V[k] * V[n] * Y_mag * np.sin(theta_kn + angle_diff)
    P_yx.append(Pk)
    Q_yx.append(Qk)

# --- Step 6: Form calculated vector yx ---
yx_pu = np.array(P_yx + Q_yx)

# --- Step 7: Compute mismatch vector ---
delta_y = y_pu - yx_pu

# --- Step 8: Print results for inspection ---
print("\n--- INITIALIZED y (Specified Power Vector) ---")
for i, val in enumerate(y_pu):
    print(f"y[{i}] = {val:.6f}")
print(f"[DEBUG] y shape = {y_pu.shape}")

print("\n--- CALCULATED yx (Injected Power Vector) ---")
for i, val in enumerate(yx_pu):
    print(f"yx[{i}] = {val:.6f}")
print(f"[DEBUG] yx shape = {yx_pu.shape}")

print("\n--- MISMATCH Vector Δy = y - yx ---")
for i, val in enumerate(delta_y):
    print(f"Δy[{i}] = {val:.6f}")
print(f"[DEBUG] del_y shape = {delta_y.shape}")

