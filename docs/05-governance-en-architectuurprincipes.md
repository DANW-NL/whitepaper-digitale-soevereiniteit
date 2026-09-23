# 5 Governance- en architectuurprincipes
Voor architecten kunnen principes een middel zijn om het gesprek over digitale soevereiniteit concreet te maken. Zij helpen om abstracte ambities te vertalen naar ontwerpkeuzes en om bestuurlijke discussies te verbinden met de technische en organisatorische realiteit.

De principes in dit hoofdstuk zijn bedoeld als richtinggevend kader voor architecten en besluitvormers. Ze zijn zo opgesteld, dat ze iedere organisatie ruimte laten voor proportionele concretisering naar architectuurkeuzes, passend bij de context van de eigen organisatie, de mate waarin waardestromen bedrijfskritisch zijn, de dataclassificatie, de afhankelijkheden in de keten en de risicotolerantie.

De kans is groot, dat de principes voor digitaalkundige architecten herkenbaar zijn. Vreemd is dat niet, want als algemene uitgangspunten voor goed ontwerp gelden ze ook voor aspecten zoals continuïteit, informatiebeveiliging en privacy.

## 5.1 Maak kritieke afhankelijkheden expliciet
Een eerste en fundamenteel principe is dat kritieke afhankelijkheden zichtbaar moeten worden gemaakt. Veel organisaties zijn in de loop der jaren afhankelijk geworden van leveranciers, platforms, diensten, technologieën en regio’s zonder dat deze afhankelijkheden expliciet zijn benoemd of bestuurd. Juist daardoor worden risico’s vaak pas zichtbaar wanneer er zich een incident, prijsverhoging, contractueel geschil, geopolitieke verandering of technische blokkade voordoet.

Voor digitale soevereiniteit is het daarom noodzakelijk om systematisch in kaart te brengen van welke externe partijen en voorzieningen een organisatie afhankelijk is, hoe diep die afhankelijkheid reikt en welke gevolgen het heeft wanneer deze wegvalt of verandert. Het gaat daarbij niet alleen om primaire IT-diensten, maar ook om onderliggende bouwstenen zoals werkplekdiensten, platformdiensten, logisch toegangsbeheer, cryptografie, beheertools, dataopslag, externe (beheer-)diensten, netwerkvoorzieningen, rekenkracht, fysieke apparatuur.

Architectuur moet deze afhankelijkheden niet alleen registreren, maar ook duiden. Een afhankelijkheid is pas bestuurbaar wanneer duidelijk is welke risico’s eraan verbonden zijn en of deze acceptabel, te mitigeren of onwenselijk zijn. Dit principe vormt daarmee het vertrekpunt voor alle verdere afwegingen in digitale soevereiniteit.

## 5.2 Hanteer proportionaliteit op basis van kritische belangen
Niet elke voorziening hoeft maximaal soeverein te worden ingericht. Een generieke kantoorfunctie stelt andere eisen dan een bedrijfskritische waardestroom, een vitale overheidsdienst of een proces waarin gevoelige gegevens, publieke waarden of hoge continuïteitseisen een rol spelen. Daarom dient digitale soevereiniteit altijd proportioneel benaderd te worden.

Dit betekent dat organisaties hun eisen aan autonomie, controle en beheersbaarheid in de praktijk zullen differentiëren op basis van de kritische belangen. Hoe groter de impact van verstoring, ongewenste toegang, dataverlies of lock-in, des te zwaarder de eisen die aan de architectuur moeten worden gesteld. De kritische belangen kunnen daarbij voortkomen uit operationele impact, maatschappelijke gevolgen, wettelijke verplichtingen, financiële schade, reputatierisico, afhankelijkheid van ketenpartners of effecten op bestuurlijke controle.

Voor architecten betekent dit principe dat ontwerpkeuzes niet los mogen worden beoordeeld, maar altijd in relatie tot de aard van het proces, de data en de afhankelijkheden die ermee samenhangen. Proportionaliteit voorkomt enerzijds overspecificatie en onnodige kosten, en anderzijds onderschatting van risico’s in kritieke omgevingen.

## 5.3 Ontwerp voor interoperabiliteit en openheid
Digitale soevereiniteit wordt versterkt wanneer systemen, diensten en gegevensuitwisselingen gebaseerd zijn op open, overdraagbare en breed toepasbare afspraken. Interoperabiliteit is daarom een kernprincipe. Organisaties die hun architectuur op alle lagen baseren op gestandaardiseerde interfaces, open gegevensmodellen en helder gedefinieerde koppelvlakken, behouden meer wendbaarheid dan organisaties die sterk leunen op leveranciersgebonden integraties of gesloten platformvoorzieningen.

Dit principe betekent niet dat alleen open source of uitsluitend open standaarden zijn toegestaan. Wel betekent het dat architecten bewust moeten afwegen in hoeverre keuzes leiden tot technische of functionele lock-in. Wanneer een oplossing alleen goed functioneert binnen één leverancier specifiek ecosysteem, neemt de afhankelijkheid toe en wordt eventuele vervanging lastiger. Interoperabiliteit verlaagt die drempel en vergroot de ruimte om in de toekomst te migreren, te combineren of te vervangen.

Voor digitale soevereiniteit is openheid vooral van belang bij dataopslag, logische toegangsbeveiliging, toegankelijkheid van de data zelf, en portabiliteit van functionaliteit. Het ontwerp moet daarom voorkomen dat kernprocessen onnodig worden verankerd in gesloten mechanismen waarvoor geen reëel alternatief beschikbaar is.

## 5.4 Beperk lock-in door modulariteit en vervangbaarheid
Een toekomstbestendige architectuur is modulair van opzet. Dat betekent dat functies, data, integraties en technische voorzieningen zoveel mogelijk zodanig worden ingericht dat zij afzonderlijk kunnen worden aangepast of vervangen zonder disproportionele impact op de rest van het landschap. Modulariteit is daarmee een praktisch antwoord op ongewenste vendor lock-in.

Voor digitale soevereiniteit is vervangbaarheid een aspect dat extra aandacht vraagt. Een organisatie hoeft niet iedere component op korte termijn te kunnen uitwisselen, maar moet wel weten welke onderdelen feitelijk niet vervangbaar zijn en waarom. Waar een leverancier of platform een unieke en diep verweven positie heeft in een bedrijfskritische waardestroom, moet dit expliciet worden afgewogen en bestuurlijk worden gedragen.

Architecten kunnen dit principe concreet maken door te ontwerpen met duidelijke scheidingen tussen businesslogica, data, integratie, identity, beheer en infrastructuur. Ook helpt het om zoveel mogelijk te sturen op contractuele en technische vervangbaarheid, exporteerbaarheid van data, overdraagbaarheid van configuraties en beperking van afhankelijkheid van unieke platformservices wanneer daar geen proportionele rechtvaardiging voor bestaat.

## 5.5 Borg regie op data, sleutels en toegang
Digitale soevereiniteit raakt direct aan de vraag wie feitelijk controle heeft over data en over de middelen waarmee toegang tot die data wordt verkregen. Daarom is een belangrijk ontwerpprincipe dat organisaties expliciet sturen op eigenaarschap, classificatie, locatie, toegang en bescherming van data, inclusief de inrichting van sleutelbeheer en identiteitsvoorzieningen.

Het gaat hierbij niet alleen om opslaglocatie of juridische datalocatie, maar ook om de bredere keten van verwerking, beheer, supporttoegang, replicatie, logging, back-up en herstel. Ook moet duidelijk zijn onder welke voorwaarden derden toegang kunnen krijgen tot gegevens of beheerfunctionaliteiten. Zeker bij cloud- en platformdiensten is dit een cruciaal aandachtspunt, omdat de feitelijke controle over identity, sleutelbeheer en privileged access mede bepaalt in hoeverre een organisatie daadwerkelijk autonoom opereert.

Voor architecten betekent dit dat regie op data niet mag worden gereduceerd tot een privacy- of complianceonderwerp. Het is een ontwerpvraagstuk dat raakt aan de kern van digitale autonomie. Waar de organisatie de feitelijke controle over data, sleutels of toegang verliest, bestaat het risico dat ze alle zeggenschap over de eigen data kwijtraakt, ook als de functionele dienstverlening intact blijft.

## 5.6 Ontwerp voor continuïteit, herstelbaarheid en vervangbaarheid
Digitale soevereiniteit wordt pas werkelijk relevant wanneer omstandigheden veranderen. Een leverancier kan diensten wijzigen of beëindigen, toegang kan worden beperkt, geopolitieke verhoudingen kunnen verschuiven, of een organisatie kan genoodzaakt zijn een andere koers te kiezen. Daarom moet architectuur niet alleen gericht zijn op normaal gebruik, maar juist ook op verstoring, herstel en vervangbaarheid.

Dit principe vraagt dat organisaties al in het ontwerp nadenken over scenario’s waarin diensten niet of slechts beperkt beschikbaar zijn, communicatieketens verstoord raken of data en functionaliteit elders moeten worden ondergebracht. Het gaat dan om vragen als: wat gebeurt er bij langdurige uitval, welke processen moeten blijven functioneren, welke gegevens moeten beschikbaar blijven, hoe snel moet kunnen worden hersteld, en hoe realistisch is het om een voorziening daadwerkelijk te verlaten?

Vervangbaarheid mag daarbij niet uitsluitend contractueel worden benaderd. Een contractuele clausule om een afgenomen dienst te kunnen migreren naar een andere leverancier zonder technische uitvoerbaarheid biedt schijnzekerheid. Architectuur moet daarom ook zicht geven op de mate van exporteerbaarheid van data, afhankelijkheid van specifieke configuraties, benodigde migratiestappen, overdraagbaarheid van kennis en de operationele impact van een overstap. Continuïteit, herstelbaarheid en vervangbaarheid zijn in dat opzicht geen sluitstuk, maar fundamentele ontwerpeisen aan elke digitale oplossing.

## 5.7 Veranker besluitvorming in expliciete risicokaders
Digitale soevereiniteit vraagt om keuzes die zelden zwart-wit zijn. Er is vaak sprake van een afweging tussen gebruiksgemak, kosten, snelheid, continuïteit en autonomie. Om te voorkomen dat dergelijke keuzes willekeurig of incident-gedreven worden gemaakt, moeten zij worden ingebed in expliciete risicokaders.

Een belangrijk ontwerpprincipe is daarom dat architectuurbesluiten over afhankelijkheden en autonomie toetsbaar moeten zijn aan vooraf bepaalde kaders, zoals een model voor risicotolerantie. Daarmee wordt zichtbaar welke mate van afhankelijkheid nog acceptabel is, welke mitigerende maatregelen verplicht zijn en wanneer escalatie of bestuurlijke besluitvorming nodig is.

Voor architecten heeft dit twee voordelen:

1. Er ontstaat meer consistentie in besluitvorming tussen projecten, domeinen en waardestromen.
2. Uitzonderingen worden beter uitlegbaar. Niet elke keuze voor een buitenlandse cloudvoorziening die leidt tot een afhankelijkheid hoeft onwenselijk te zijn, maar dergelijke keuzes moeten wel bewust, navolgbaar en aantoonbaar binnen de afgesproken kaders passen.

## 5.8 Borg transparantie en toetsbaarheid in governance
Een architectuur die digitale soevereiniteit ondersteunt, vraagt om governance die inzicht geeft in gemaakte keuzes, resterende risico’s en de werking van mitigerende maatregelen. Transparantie is daarmee niet alleen een bestuurlijk beginsel, maar ook een ontwerpprincipe. Wanneer een organisatie niet kan uitleggen hoe afhankelijkheden zijn georganiseerd, welke datastromen bestaan, welke toegangspaden actief zijn en welke restrisico’s zijn geaccepteerd, ontbreekt de basis voor effectieve sturing.

Dit principe vraagt om een architectuur waarin relevante informatie over leveranciers, integraties, datastromen, toegangsmodellen, classificaties en maatregelen vindbaar en actualiseerbaar is. Ook moeten de uitkomsten van beoordelingen periodiek kunnen worden herzien, omdat technologische en geopolitieke omstandigheden veranderen. Wat vandaag proportioneel en acceptabel is, kan morgen een te groot risico vormen.

Toetsbaarheid betekent dat architectuurkeuzes niet alleen op ontwerpmomenten worden besproken, maar ook in beheer en governance een plaats krijgen. Digitale soevereiniteit moet zichtbaar zijn in architectuurreviews, in risicobeoordelingen, in sourcingbesluiten en in de verantwoording aan bestuur en toezicht.

## 5.9 Soevereiniteit ‘by-design’
Experimentele trajecten, pilots en proof-of-concepts (PoC’s) zijn waardevol om nieuwe technologie te verkennen, maar kunnen ook nieuwe afhankelijkheden introduceren. Daarom moeten soevereiniteitsprincipes al vanaf experiment en ontwerp worden meegewogen.

Tegelijk kunnen experimentele trajecten ook worden gebruikt om alternatieve technologieën of diensten, complexiteitsreductie en vervangingsscenario’s vroegtijdig te toetsen. Door deze eerst als innovaties, PoC's of pilots neer te zetten, kan de haalbaarheid in een vroeg stadium worden getoetst.

Juist in situaties waar vervanging van een bestaande dienst of oplossing een meerjarig en duur traject dreigt te worden, kan het interessant zijn te verkennen welke complexiteitsreductie en tastbare resultaten te behalen zijn via experimentele, innovatieve initiatieven. Zo krijgen betrokkenen de mogelijkheid te leren hoe soevereiniteit succesvol is op te nemen in de architectuur en ontwerpen.
