import numpy as np
import matplotlib.pyplot as plt


###################################  Uppgift 1, differentialekvation ##########################

# Löser differentialekvationen numeriskt för en RLC-krets och plottar spänningen och strömmen som funktion av tiden 
# och beräknar fasvinkeln. Användaren ska, utöver att ange värden på R, L och C,
# även ge uppgifter om spänningen från spänningskällan och begynnelsevillkor. 
def solve_RLC_circuit(R, L, C, U0, initial_conditions, time):
    
    # Antal tidspunkter
    dim = len(time)
    
    # Initialisera arrayer för ström, dess derivata och andra derivatan (för numerisk lösning av diffekvation)
    current = np.zeros(dim)
    current_derivate = np.zeros(dim)
    current_2derivate = np.zeros(dim)
    
    # Initialvärden för ström och dess derivata
    current[0] = initial_conditions[0]
    current_derivate[0] = initial_conditions[1]
    
    # Värden för omega (test med 800) och tidssteg
    omega = 800
    dt = 1e-6
    
    # Impedansen Z och I0 mha formeln för impedans i en RLC-krets
    Z = np.sqrt(R**2 + (1/(omega*C) - omega*L)**2)
    I0 = U0 / Z    
    
    # Analytiska lösningen för strömmen I(t) mha formeln för en sinusformad ström (för att jämföra med analytisk)
    phi = np.arctan((1/(omega*C) - omega*L) / R)
    current_analytical = I0 * np.sin(omega * time + phi)
    
    # Begynnelsevillkor för strömmen och dess derivata
    current[0] = I0  
    current_derivate[0] = -omega * U0 * np.cos(omega * time[0]) / R 
    
    # Numerisk lösning med Euler-metoden
    for i in range(dim - 1):
        current_2derivate[i] = (U0 * omega * np.cos(omega * time[i]) - R * current_derivate[i] - current[i] / C) / L
        current_derivate[i+1] = current_derivate[i] + current_2derivate[i] * dt
        current[i+1] = current[i] + current_derivate[i] * dt
        
    # Spänningen med hjälp av formeln för spänningen i en sinusformad krets
    voltage = U0 * np.sin(omega * time)
    
    # Returnera värden för att plotta de
    return voltage, current, current_analytical, Z, time

###################################### Plotta differential ekvationen #######################################

def plot_voltage_current(voltage, current, current_analytical, Z, time):
    # Plotta spänning och ström som funktion av tiden
    plt.plot(time, voltage, label='Spänning')
    plt.plot(time, Z * current_analytical, label='Z * I(t) analytisk', linestyle='--')
    plt.plot(time, Z * current, label='Z * I(t) numerisk')
    plt.xlabel('Tid (s)')
    plt.ylabel('Amplitud (V)')
    plt.legend()
    plt.grid(True)
    plt.show()
    
######################################  Fasvinkel  ############################################ 

    # Beräknar fasvinkeln för en RLC-krets
    # Implementera formel för fasvinkel här
def calculate_phase_angle(R, L, C):
    omega = 800

    # Beräkna fasvinkeln
    tan_phase_angle = ((1 / (omega * C)) - omega * L) / R
    phase_angle = np.arctan(tan_phase_angle) * (180/np.pi) 

    return phase_angle

#############################################  Uppgift 2  ################################################################

# Beräknar överföringsfunktionen för en komponent i RLC-kretsen
def calculate_transfer_function(component, R, L, C, w):
    Z = np.sqrt(R ** 2 + (1 / (w * C) - w * L) ** 2) #räknar ut impedans

    if component == 'L': #Om användaren väljer spole
        H = w * L / Z
    elif component == 'R': #Om användaren väljer resistor
        H = R / Z
    elif component == 'C': #Om användaren väljer kondensator
        H = (1 / (w * C)) / Z
    else:
        print("Felaktig komponent. Skriv R, L, eller C.")
        return

    return H

# Funktion för att plotta överföringsfunktionen för en komponent
def plot_transfer_function(component, R, L, C, w_values):
    H_values = [] #skapar en tom lista för alla överföringsfunktioner.

    for w in w_values: #loopar igenom vaje väre av w i w_values
        H = calculate_transfer_function(component, R, L, C, w) #Beräknar överföringsfunktionen för angivna komponent vid w
        H_values.append(H) #Lägger till det beräknade överföringsfunktionsvärdet till listan H_values

    w_over_w0 = w_values / 540 #1/sqrLC  =w0

    plt.plot(w_over_w0, H_values)

    plt.title('Överföringsfunktionen H(w) för ' + component) 
    plt.xlabel('w / w0')
    plt.ylabel('H(w)')
    plt.grid(True)
    plt.show()



##########################################  uppgift 3 ############################################

#plottar en överföringsfunktion (filterfunktionen) för ett analogt filter baserat på en RLC-krets 
# och optimerar resistansen så att överföringsfunktionen blir så jämn som möjligt
# Funktion för att beräkna överföringsfunktionen för filtret
def calculate_function(R, L, C, w):
    Z = np.sqrt(R ** 2 + (1 / (w * C) - w * L) ** 2) #räknar ut impedans
    H = w * L / Z #räknar ut överföringsfunktionen för spole
    return H #returnerar överföringsfunktionen 

# Funktion för att plotta överföringsfunktionen för filtret och optimera resistansen
def plot_optimized_transfer_function(R, L, C, w_values,filter_type):
    omega_0 = 1 / np.sqrt(L * C)  # Resonansfrekvensen

    # Optimera resistansen för att minimera kostnaden
    optimal_R = optimize_resistance(L, C, omega_0, w_values,filter_type)
    w_over_w0 = w_values / 540 #1/sqrLC  =w

    # Beräkna överföringsfunktionen med det optimala R-värdet
    H_values_optimal = calculate_function(optimal_R, L, C, w_values) 

    # Plotta överföringsfunktionen
    plt.figure(figsize=(10, 6))
    plt.plot(w_over_w0, H_values_optimal, label=f'Optimerad R = {optimal_R:.2f} Ohm')
    plt.xlabel('w / w0')
    plt.ylabel('H(w)')
    plt.grid(True)
    plt.legend()
    plt.show()

# Funktion för att optimera resistansen för att minimera kostnaden (MSE)
def optimize_resistance(L, C, omega_0, omega_range, filter_type):
    R_min = 1  # Lägsta möjliga resistans
    R_max = 1000  # Högsta möjliga resistans
    num_steps = 100  # Antal steg i sökområdet

    best_cost = np.inf  # Bästa kostnaden initieras till oändlighet
    best_R = R_min  # Anta att lägsta möjliga R-värde är det bästa

    if filter_type == 'L':
        # Vid lågpassfilter vill vi ha lägre resistans
        R_min = 1
        R_max = 200
    elif filter_type == 'H':
        # Vid högpassfilter vill vi ha högre resistans
        R_min = 200
        R_max = 1000

    for R in np.linspace(R_min, R_max, num_steps):
        # Beräkna överföringsfunktionen för det aktuella R-värdet
        H_values = calculate_function(R, L, C, omega_range)
        # Beräkna kostnaden (MSE) mellan faktisk överföringsfunktion och önskad funktion
        current_cost = cost_function(H_values, omega_range, omega_0)

        # Jämför den aktuella kostnaden med den bästa (lägsta) kostnaden hittills
        if current_cost < best_cost:
            best_cost = current_cost
            best_R = R

    return best_R

# Funktion för att beräkna kostnaden (MSE) mellan faktisk överföringsfunktion och önskad funktion
def cost_function(H_values, omega_range, omega_0):
    # Skapa Ideal funktion: 0 för frekvenser ≤ omega_0 (lågpass), 1 för frekvenser > omega_0 (högpass).
    target_function = np.where(omega_range <= omega_0, 0, 1)
    # Beräkna medelkvadratfelet (MSE) mellan faktisk överföringsfunktion och önskad funktion
    cost = np.mean((H_values - target_function)**2)
    return cost

  

######################################  Huvudprogrammet #############################################
def main():
    print("-------------------------------------------------------------------------\n\n")
    print("1. Lösa differentialekvationer numeriskt för en RLC-krets, plotta spänningen och strömmen som en funktion av tiden samt beräkna fasvinkeln. ")
    print("2. Plotta en överföringsfunktion för någon av komponenterna i en RLC-krets.")
    print("3. Plotta en överföringsfunktion för ett analogt filter baserat på en RLC-krets och optimerar resistansen så att överföringsfunktionen blir så jämn som möjligt. \n")

    option = int(input("Ange ditt val: "))

    # Om användaren väljer att lösa differentialekvationen för en RLC-krets
    if option == 1:
        # Användarens input för uppgift 1
        R = float(input("Ange resistans (R): "))
        L = float(input("induktans (L): "))
        C = float(input("kapacitans (C): "))
        U0 = float(input("spänning från källan (U0): ")) 

        dt = 1e-6
        tmax = 0.08
        t_values = np.arange(0, tmax, dt)  # Definiera tidsstegen här
        omega = 800

        # Löser differentialekvationen och plottar spänning och ström
        initial_conditions = [U0 / np.sqrt(R ** 2 + ((1 / (omega * C)) - (omega * L)) ** 2), 0.0]
        
        
        voltage, current, current_analytical, Z, time = solve_RLC_circuit(R, L, C, U0, initial_conditions, t_values) 
        plot_voltage_current(voltage, current, current_analytical, Z, time)
        
        # Beräknar och skriver ut fasvinkeln
        phase_angle = calculate_phase_angle(R, L, C)
        print("Fasvinkel:", phase_angle, "grader")
  

    # Om användaren väljer att plotta överföringsfunktionen för en komponent i RLC-kretsen
    elif option == 2:
        # Användarens input för uppgift 2
        component = input("Ange komponent (R, L, eller C): ")
        R = float(input("resistans (R): "))
        L = float(input("induktans (L): "))
        C = float(input("kapacitans (C): "))
        
        # Värden för w och w0
        #w0 = 1 / np.sqrt(L * C)
        w = 800
        w_values = np.linspace(0.0, 3.0, 1000) * w

        # Plotta överföringsfunktionen för komponenten
        plot_transfer_function(component, R, L, C, w_values)
        

    # Om användaren väljer att plotta överföringsfunktionen för ett analogt filter baserat på en RLC-krets och optimera resistansen
    elif option == 3:
        # Användarens input för uppgift 3
        R = float(input("resistans (R): "))
        L = float(input("induktans (L): "))
        C = float(input("kapacitans (C): "))
        filter_type = input("Ange filtertyp (Lågpass (L) eller Högpass (H)): ").capitalize()


        w = 800
        w_values = np.linspace(0.0, 3.0, 1000) * w
        
        # Plottar överföringsfunktionen för filtret
        plot_optimized_transfer_function(R, L, C, w_values, filter_type)

    else:
        print("fel")

# så att main körs
if __name__ == "__main__":
    main()