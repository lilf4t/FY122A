# Problembeskrivning
Satelliter används idag flitigt, både för kommersiell användning (väder, telekommunikation, etc.)
och för forskningsändamål. Ibland behöver två satelliter kopplas ihop, vilket benämns att satelli-
terna dockar. Uppgiften går ut på att skriva en funktion till ett enkelt simuleringsprogram som körs i Python.
Före, under och efter dockningen så rör sig satelliterna enligt fysikens lagar. Funktionen ska in-
nehålla den fysikaliska delen av dockningen. Vi gör här antagandet att alla yttre krafter, såsom
gravitationskrafter från jorden, kan försummas. Vidare försummar vi att satelliterna rör sig i om-
loppsbanor runt jorden, och antar istället att satelliterna rör sig längs räta linjer.
I simuleringsprogrammet antas att den ena satelliten befinner sig i vila, medan den andra kan
röra sig i en dimension genom att påverkas av (raket)krafter framåt eller bakåt. Storleken av
kraftpåverkan bestäms av användaren av simuleringsprogrammet. Vid anrop av funktionen finns i
in-variablerna kännedom om satelliternas läge och hastighet vid tiden t, samt storleken på den kraft
som påverkar den ena satelliten och tidstegets storlek. Funktionens uppgift är att bestämma båda
satelliternas lägen och hastigheter vid tiden t + ∆t, där ∆t är ett litet tidssteg. Speciellt ska funk-
tionen bestämma om dockning sker inom tidssteget, och i så fall bestämma hur det sammansatta
systemet rör sig efter dockningen.
För att dockningen ska lyckas så krävs, förutom att satelliterna kommer i kontakt, att satelliternas
inbördes relativa hastighet inte är alltför stor. Om detta är uppfyllt kan dockningen fysikaliskt sett
betraktas som en (fullständigt) inelastisk stöt. Om istället den relativa hastigheten är för stor, så
antas att satelliterna genomgår en elastisk kollision, utan att docka.
Mer information om dockningen finns i kommentarerna i simuleringsprogrammet. Uppdateringen
av variablerna sker i början av filen
