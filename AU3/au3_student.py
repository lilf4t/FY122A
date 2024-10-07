# @author- Fatima Kadum

from math import radians, cos, sin, asin, acos
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid # pip install scipy i terminalen

latitude = 57.6  # Solpanelens latitud φ (grader) i Visby
panel_altitude = 55  # Solpanelens lutning i grader (θp)
panel_azimuth = 210  # Orientering av solpanel i grader (αp)
epsilon = 0.15  # Verkningsgrad för solpanel
A = 50  # Ytan av solpanel i kvadratmeter
solar_constant = 1360  # Solkonstant i W/m2
dt = 0.1  # Tidssteg

###################################################################################################################################

# Funktion för att beräkna solens deklinationsvinkel för en given dag på året (ekvation 2)
def calculate_declination_angle(day):
    return radians(-23.44) * cos(radians(360 * day / 365))

# Funktion för att beräkna solens altitud θs för en given tid på dagen och dag på året (ekvation 1)
def calculate_altitude_angle(hour, day):
    declination = calculate_declination_angle(day)
    hour_angle = radians(15) * hour - radians(180)  # (ekvation 3)
    return asin(sin(radians(latitude)) * sin(declination) + cos(radians(latitude)) * cos(declination) * cos(hour_angle))

# Funktion för att beräkna solens azimut vinkel (αs) i grader, för en given tid på dagen och dag på året
def calculate_azimuth_angle(hour, day):
    hour_angle = radians(15) * hour - radians(180) # (ekvation 3)
    declination = calculate_declination_angle(day)
    theta = calculate_altitude_angle(hour, day)
    cos_term = round((sin(radians(latitude)) * sin(theta) - sin(declination)) / (cos(radians(latitude)) * cos(theta)), 4)
    if hour_angle < 0:
        azimuth = radians(180) - acos(cos_term) # (ekvation 4)
    else:
        azimuth = radians(180) + acos(cos_term) # (ekvation 4)
    return azimuth

"########################################## Uppgift 1 ########################################"
'''
1. Skapa plottar som visar effekten i Watt [W] som funktion av tiden på dygnet för er grupps
stationära solpanel (se tabell 1) för ett dygn i januari och i juni. Ni ska inte ta hänsyn till
antalet soltimmar, d.v.s. anta alltid soligt väder (se figur 2 i appendix A för exempel).
'''

# Funktion för att beräkna effektuttaget från solpanelen för en given tid på dagen och dag på året
# Använder solens altitud och azimutvinkel
def task_1():
    def calculate_power_output(hour, day):
        # Beräkna solens altitud (θs) och azimutvinkel (αs)
        solar_altitude = calculate_altitude_angle(hour, day)
        solar_azimuth = calculate_azimuth_angle(hour, day)
        
        # Beräkna solinstrålningen (I)  
        if solar_altitude < 0:
            I = 0
        else:
            I = 1.1 * solar_constant * 0.7 ** ((1 / sin(solar_altitude)) ** 0.678) # (ekvation 5)
            I = max(I, 0)  # Säkerställ att strålningen inte är negativ
        
        # Beräkna effektuttaget från solpanelen # (ekvation 6)
        panel_I = I * (
            cos(radians(panel_altitude) - solar_altitude) * 
            cos(radians(panel_azimuth) - solar_azimuth) + 
            (1 - cos(radians(panel_azimuth) - solar_azimuth)) * 
            sin(radians(panel_altitude)) * 
            sin(solar_altitude)
        )
        panel_I = max(panel_I, 0)  # Säkerställ att strålningen inte är negativ
        
        real_power_output = epsilon * panel_I * A # (ekvation 7)
        perfect_power_output = epsilon * I * A   
        
        return real_power_output, perfect_power_output

    # Skapa plottar för 1 januari och 1 juni
    hours = np.arange(0, 23, 0.1)
    days = [1, 153] #1 jan o 1 jun
    specific_hour = 14.5  # 14:30

    for day in days:
        power_outputs = [calculate_power_output(hour, day) for hour in hours]
        real_power_lists = [power[0] for power in power_outputs]  # Använd [0] för att välja real_power_output
        perfect_power_lists = [power[1] for power in power_outputs]  # Använd [1] för att välja perfect_power_output
        plt.plot(hours, perfect_power_lists, linestyle='--', color='black', label='Tillgänglig')
        plt.plot(hours, real_power_lists, color='blue', label='Panel')
        specific_power_output = calculate_power_output(specific_hour, day)[0]  # För att plotta tiden
        plt.scatter(specific_hour, specific_power_output, color='blue', marker='o', label=f'Panel 14:30')
        plt.xlabel("t(h)")
        plt.ylabel("P(W)")
        plt.ylim(0, None)
        plt.grid()
        plt.legend()
        
        # Sätt titlar för plottarna baserat på index i loopen
        if day == 1:
            plt.title("1 januari")
        else:
            plt.title("1 juni")
        
        plt.show()

"########################################## Uppgift 2  ########################################"
'''
2. Beräkna energin i kWh som en stationär solpanel för er grupp (se tabell nedan) levererar
under januari månad, juni månad och under ett helt år. Ni ska utföra beräkningarna både
med och utan hänsyn taget till antalet soltimmar. 
'''

# Beräkna effektuttaget från solpanelen för en given tid på dagen och dag på året
def task_2():
    def calculate_power_output(hour, day):
        # Beräkna solens altitud (θs) och azimutvinkel (αs)
        solar_altitude = calculate_altitude_angle(hour, day)
        solar_azimuth = calculate_azimuth_angle(hour, day)
        
        # Beräkna solinstrålning (I)
        if solar_altitude < 0:
            I = 0
        else:
            I = 1.1 * solar_constant * 0.7 ** ((1 / sin(solar_altitude)) ** 0.678) # (ekvation 5)
            I = max(I, 0)  # Säkerställ att strålningen inte är negativ
        
        # Beräkna effektutaget från solpanelen # (ekvation 6)
        panel_I = I * (cos(radians(panel_altitude) - solar_altitude) * cos(radians(panel_azimuth) - solar_azimuth) 
                        + (1 - cos(radians(panel_azimuth) - solar_azimuth)) * 
                        sin(radians(panel_altitude)) * sin(solar_altitude))
        
        panel_I = max(panel_I, 0)  # Säkerställ att strålningen inte är negativ
        
        real_power_output = epsilon * panel_I * A / 1000  # (ekvation 7, få ut i kWh)
        return real_power_output, I

    plt.figure()
    plt.text(0.5, 0.5, 'Se terminalutskrift för uppgift 2', horizontalalignment='center', verticalalignment='center', fontsize=20)
    plt.axis('off')  
    plt.show()

    # Beräkna energi för given dag och tidssteg (utan hänsyn till soltimmar)
    def energy_output(day, time_step):
        # Beräkna effektuttaget för varje timme under dagen och lägg till i listan
        power_outputs = [calculate_power_output(hour, day)[0] for hour in np.arange(1, 24, time_step)] 
        # Beräkna den totala energin baserat på den beräknade effekten och använd trapezregeln för att integrera
        energy_real = trapezoid(power_outputs, dx=time_step)
        return energy_real

    # Månader och dess dagar
    months = [('Januari', range(1, 31 + 1)),
             ('Juni', range(151, 181 + 1)),
             ('hela året', range(1, 365 + 1))]

    print("--------------------------------------------------------------------------------------------------------------------------")
    print("\nEnergin (kWh) som en stationär solpanel levererar under januari, juni och under ett helt år (utan hänsyn till soltimmar):\n ")

    # Beräkna och skriv ut energin för januari, juni och hela året
    for month, days_in_month in months:
        energy_delivered = sum(energy_output(day, dt) for day in days_in_month)
        print(f'Total levererad energi för {month}: {energy_delivered:.2f} kWh')
    
    ##################################### Med hänsyn till soltimmar ############################

    # Beräkna energi för given dag och tidssteg (med hänsyn till soltimmar)
    def energy_output_sunny(day, dt, sunny_hours):
        power_outputs = []
        sun_hours = 0
        # Loopar genom varje timme med det givna tidssteget.
        for hour in np.arange(1, 24, dt):
            real_power_output, perfect_power_output = calculate_power_output(hour, day)
            power_outputs.append(real_power_output)
            # Kontrollerar om den perfekta effekten är över en viss tröskel (120 här).
            if perfect_power_output > 120:
                sun_hours += 1
        # 10 samplar/timme --> 240/dag, ska bli 24 timmar
        factor = sunny_hours / (sun_hours / 10)  
        energy_real_sunny = trapezoid(np.array(power_outputs) * factor, dx=dt)
        return energy_real_sunny

    # Soltimmar i Visby / antal dagar i månaden
    sunshine_hours_jan = 41/31   
    sunshine_hours_jun = 315/30  
    sunshine_hours_year = 2080/365 

    # Månader och dess dagar
    months = [('Januari', range(1, 31 + 1), sunshine_hours_jan),
              ('Juni', range(151, 181 + 1), sunshine_hours_jun), 
              ('Hela året', range(1, 365 + 1), sunshine_hours_year)]

    print("--------------------------------------------------------------------------------------------------------------------------")
    print("\nEnergin (kWh) som en stationär solpanel levererar under januari, juni och under ett helt år (med hänsyn till soltimmar):\n ")

    # Beräkna energi för varje dag
    # Summera energin från varje dag för att få energin per mån/år
    for month, days_in_month, sunny_hours in months:
        energy_delivered = sum(energy_output_sunny(day, dt, sunny_hours) for day in days_in_month)
        print(f'Total levererad energi för {month}: {energy_delivered:.2f} kWh')


"################################################## Uppgift 3 #######################################################"
'''
3. Optimera θp med hänsyn taget till antalet soltimmar så att levererad energi i kWh under
ett år blir så stor som möjligt för gruppens stationära solpanel. Hur stor blir den maximala
energin i kWh och vid vilken vinkel θp? Vinkeln αp enligt tabell.
'''

def task_3():
    # Samma kod från uppgift 2
    # # Beräkna effektuttaget från solpanelen för en given tid på dagen och dag på året
    def calculate_power_output(hour, day):
      # Beräkna solens altitud (θs) och azimutvinkel (αs)
      solar_altitude = calculate_altitude_angle(hour, day)
      solar_azimuth = calculate_azimuth_angle(hour, day)

      # Beräkna solinstrålning (I)
      if solar_altitude < 0:
          I = 0
      else:
          I = 1.1 * solar_constant * 0.7 ** ((1 / sin(solar_altitude)) ** 0.678) # ekvation 5
          I = max(I, 0)  # Säkerställ att strålningen inte är negativ

      # Beräkna effektutaget från solpanelen
      panel_I = I * (cos(radians(panel_altitude) - solar_altitude) * cos(radians(panel_azimuth) - solar_azimuth) 
                     + (1 - cos(radians(panel_azimuth) - solar_azimuth)) * sin(radians(panel_altitude)) * sin(solar_altitude))
      panel_I = max(panel_I, 0)  # Säkerställ att strålningen inte är negativ

      real_power_output = epsilon * panel_I * A / 1000 

      return real_power_output, I

    plt.figure()
    plt.text(0.5, 0.5, 'Se terminalutskrift för uppgift 3 (Tar lite tid)', horizontalalignment='center', verticalalignment='center', fontsize=20)
    plt.axis('off')  
    plt.show()

    # Beräkna energi för given dag och tidssteg (med hänsyn till soltimmar)
    def energy_output_sunny(day, dt, sunny_hours):
        power_outputs = []
        sun_hours = 0
        for hour in np.arange(1, 24, dt):
            real_power_output, perfect_power_output = calculate_power_output(hour, day)
            power_outputs.append(real_power_output)
            if perfect_power_output > 120:
                sun_hours += 1
        # 10 samplar/timme --> 240/dag, ska bli 24 timmar
        factor = sunny_hours / (sun_hours / 10)  
        energy_real_sunny = trapezoid(np.array(power_outputs) * factor, dx=dt)
        return energy_real_sunny

    # Soltimmar i Visby / antal dagar i månaden
    sunshine_hours_year = 2080/365 

    # Definiera intervallet av möjliga värden för θp
    panel_angle_values  = np.arange(0, 91, 1)
    # Initialisera variabler för att hålla reda på maximalt energiuttag och motsvarande θp
    max_energy_output = -np.inf
    optimal_panel_angle  = None

    # Loopa över varje värde av θp och beräkna energiuttaget
    for panel_altitude in panel_angle_values:
        energy_delivered = sum(energy_output_sunny(day, dt, sunshine_hours_year) for day in range(1, 366))
        if energy_delivered > max_energy_output:
            max_energy_output = energy_delivered
            optimal_panel_angle = panel_altitude

    # Skriv ut den maximala energin och den optimala vinkeln θp
    print("--------------------------------------------------------------------------------------------------------------------------")
    print(f"Maximala energin är {max_energy_output:.2f} kWh/år vid optimala vinkeln 0p {optimal_panel_angle}°")

"######################################### Uppgift 4  ###########################################################"
'''
4. Anta vidare att den stationära solpanelen kostar 200 000 kr att installera och att den el som
solpanelen producerar får används ’gratis’ och att underskott/överskott av el kan köpas/säljas
på elbörsen för 2 kr/kWh. Om ett hushåll där solpanelen är installerad förbrukar 14 000
kWh/år, efter hur många år har solpanelen betalat sig (jämfört med att köpa all el på
elbörsen)? Använd optimerad vinkel θp i uppgift 3 för att lösa uppgiften och ta hänsyn till
antalet soltimmar. Vinkeln αp enligt tabell.
'''
def task_4():
     #  6388.20 kWh (beräknat mha uppgift 3 koden, ändrat panel_altitude = 38)
    generated_energy_kwh = 6388.20

    # Kostnaden för att installera solpanelen
    installation_cost = 200000  # kr

    # Elpris för att köpa eller sälja överskott av el på elbörsen (per kWh)
    electricity_price = 2  # kr/kWh
    
    # Antal kWh som används av huset per år
    house_energy_kwh = 14000
    
    # Beräkna antal år för att solpanelen ska betala för sig
    payback_years = installation_cost / (generated_energy_kwh * electricity_price)
    
    # Beräkna kostnaden för att köpa all el från elbörsen under ett år
    electricity_cost_per_year = house_energy_kwh * electricity_price * payback_years
    
    print(f"\n\nDet kommer ta {round(payback_years, 1)} år för att solpanelen ska betala sig själv tillbaka.")
    print(f"Hur mycket det hade kostat att betala elbörsen under samma period det tar att betala tillbaka solpanelen: {round(electricity_cost_per_year, 1)} kr \n\n")
    
"######################################### Uppgift 5  #######################################################"
'''
5. Anta nu att solpanelen görs rörlig kring två axlar och att den förses med elmotorer så att den
kan följa solens gång exakt (θp = θs och αp = αs). Hur stor energi i kWh levererar solpanelen
på ett år nu? Beräkningar utförs med hänsyn till antalet soltimmar. Totalt kostar en sådan
panel 400 000 kr att installera. Efter hur många år har denna solpanel betalat sig (jämfört
med att köpa all el på elbörsen)? Den el som motorerna drar för att vrida solpanelen i solens
riktning kan försummas. Övriga uppgifter som i uppgift 4 ovan.
'''
def task_5():
    # I den rörliga solpanelen är θp = θs och αp = αs, så vi behöver inte beräkna panelens altitud och azimuthvinkel, beräkan bara solens.

    # Samma kod från uppgift 2
    def calculate_power_output(hour, day):
        # Beräkna solens altitud (θs) och azimutvinkel (αs)
        solar_altitude = calculate_altitude_angle(hour, day)
        solar_azimuth = calculate_azimuth_angle(hour, day)
        
        # Beräkna solinstrålning (I)
        if solar_altitude < 0:
            I = 0
        else:
            I = 1.1 * solar_constant * 0.7 ** ((1 / sin(solar_altitude)) ** 0.678)  # ekvation 5
            I = max(I, 0)  # Säkerställ att strålningen inte är negativ
        
        # Beräkna effektuttaget från solpanelen
        real_power_output = epsilon * I * A / 1000  # I * A ger effekten i W, dividera med 1000 för att få kW
        return real_power_output

    # Beräkna energi för given dag och tidssteg (med hänsyn till soltimmar)
    def energy_output_sunny(day, dt, sunny_hours):
        power_outputs = []
        sun_hours = 0
        for hour in np.arange(1, 24, dt):
            real_power_output = calculate_power_output(hour, day)
            power_outputs.append(real_power_output)
            if real_power_output > 0:  # Om solen är uppe och strålning finns
                sun_hours += 1
        # 10 samplar/timme --> 240/dag, ska bli 24 timmar
        factor = sunny_hours / (sun_hours / 10)  
        energy_real_sunny = trapezoid(np.array(power_outputs) * factor, dx=dt)
        return energy_real_sunny

    # Definiera soltimmar för hela året (samma som uppgift 4)
    sunshine_hours_year = 2080 / 365 

    # Beräkna energiuttaget för ett år (med hänsyn till soltimmar)
    energy_delivered = sum(energy_output_sunny(day, dt, sunshine_hours_year) for day in range(1, 366))

    # Kostnaden för att installera solpanelen
    installation_cost = 400000  # kr

    # Elpris för att köpa eller sälja överskott av el på elbörsen (per kWh)
    electricity_price = 2  # kr/kWh
    
    # Antal kWh som används av huset per år
    house_energy_kwh = 14000

    # Beräkna antal år för att solpanelen ska betala för sig
    payback_years = installation_cost / (energy_delivered * electricity_price)
    
    # Beräkna kostnaden för att köpa all el från elbörsen under ett år
    electricity_cost_per_year = house_energy_kwh * electricity_price * payback_years
    
    print(f"--------------------------------------------------------------------------------------------------------------------------")
    print(f"\n\nEnergin (kWh) som solpanelen levererar på ett år: {energy_delivered:.2f} kWh/år")
    print(f"Det kommer att ta {round(payback_years, 1)} år för att solpanelen ska betala sig själv tillbaka.")
    print(f"Hur mycket det hade kostat att betala elbörsen under samma period det tar att betala tillbaka solpanelen: {round(electricity_cost_per_year, 1)} kr\n\n")
    
"#################################################### Main #########################################################"
    
def main():
    print("1. Visa plott av effekten i Watt [W] som funktion av tiden på en dag i Visby för vår stationära solpanel för 1 januari och 1 juni")
    print("2. Beräkna energin i kWh som vår stationär solpanel levererar under januari månad, juni månad samt under ett helt år i Visby. Både med utan hänsyn till soltimmar")
    print("3. Optimera solpanelens altitud vinkel θp med hänsyn taget till antalet soltimmar så att levererad energi i kWh under ett år blir så stor som möjligt för vår station")
    print("4. Beräkna efter hur många år solpanelen betalat sig jmf med att köpa all el på elbörsen.")
    print("5. Beräkna hur stor energi kWh solpanelen levererar på ett år om solpanelen görs rörlig kring två axlar och att den förses med elmotorer så den följer solens gång.")

    choice = input("Välj mellan (1/2/3/4/5): ")

    if choice == '1':
        task_1()
    elif choice == '2':
        task_2()
    elif choice == '3':
        task_3()
    elif choice == '4':
        task_4()
    elif choice == '5':
      task_5()
    else:
        print("Fel, välj mellan uppgift 1-5")
        
if __name__ == "__main__":
    main()

