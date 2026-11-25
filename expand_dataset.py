import os
import sqlite3

DB_PATH = "/Users/bindanm/IndicSent-M/memes.db"

# 360 Curated, High-Quality, Linguistically Balanced Memes (72 per Language x 5 Languages)
# Exactly 120 Positive, 120 Neutral, 120 Negative (24 of each class per language)

TELUGU_MEMES = [
    # Positive (24)
    {"lang": "Telugu", "tag": "Tollywood Punch", "title": "First Try Compile Success", "caption": "వామ్మో! ఈ కోడ్ ఫస్ట్ అటెంప్ట్‌లోనే రన్ అయింది! 😂🔥", "emoji": "🤯", "sentiment": "positive", "slug": "ch"},
    {"lang": "Telugu", "tag": "Pushpa Vibe", "title": "Thaggedhe Le Deployment", "caption": "టెస్టింగ్ చేయకుండానే ప్రొడక్షన్ లో డిప్లాయ్ చేశాం.. తగ్గేదే లే! 🪓🔥", "emoji": "🪓", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Balayya Power", "title": "Single Click Bugfix", "caption": "సింగిల్ క్లిక్ తో 50 బగ్స్ క్లియర్ చేసి వీకెండ్ బిర్యానీ తింటున్న మూడ్ 🍗😎", "emoji": "🍗", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "RRR Celebration", "title": "Natu Natu Signoff", "caption": "క్లయింట్ సైలెంట్ గా సైన్ ఆఫ్ ఇచ్చేశాడు.. ఇక నాటు నాటు డాన్సే! 🕺🏆", "emoji": "🕺", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Weekend Vibe", "title": "Friday Logout Bliss", "caption": "శుక్రవారం సాయంత్రం 5 గంటలకు స్లాక్ లో ఆఫ్లైన్ పెట్టే ఆనందం వేరురా బాబు 🎉🍻", "emoji": "🎉", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Ali Comedy", "title": "Google Copy Paste Win", "caption": "ఇంటర్య్వూలో 5 ఇయర్స్ సీనియర్ డెవలపర్ అని చెప్పి.. గూగుల్ లో లూప్ ఎలా రాయాలో వెతుకుతున్న నేను 💻", "emoji": "💻", "sentiment": "positive", "slug": "rollsafe"},
    {"lang": "Telugu", "tag": "Brahmi Joy", "title": "Appraisal Letter Received", "caption": "అనుకున్నదానికంటే ఎక్కువ హైక్ వచ్చింది.. ఇక పార్టీ టైమ్ రా బాబు! 🥳💰", "emoji": "🥳", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Mahesh Babu Swag", "title": "Clean Code Architecture", "caption": "నా కోడ్ చూసి సీనియర్ ఆర్కిటెక్ట్ కూడా ఫిదా అయ్యాడు.. అది నా బ్రాండ్! ✨💼", "emoji": "✨", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Chiranjeevi Energy", "title": "Feature Demo Roaring Success", "caption": "డెమో లో క్లయింట్ క్లాప్స్ కొట్టాడు.. సూపర్ హిట్ రా మామా! 👏🌟", "emoji": "👏", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Trivikram Dialouge", "title": "Elegant One Liner Fix", "caption": "మాటల్లో ప్రాస, కోడ్ లో లాజిక్.. రెండూ మనకు వెన్నతో పెట్టిన విద్య! 🎯💡", "emoji": "🎯", "sentiment": "positive", "slug": "rollsafe"},
    {"lang": "Telugu", "tag": "Allu Arjun Style", "title": "Zero Bug Delivery", "caption": "స్ప్రింట్ పూర్తయింది, జీరో బగ్స్.. తగ్గేదే లే అసలు! 🚀🏆", "emoji": "🚀", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Hyd Biryani", "title": "Paradise Biryani Treat", "caption": "ప్రాజెక్ట్ డెలివరీ అయిపోయింది.. బావార్చి లో డబుల్ మసాలా బిర్యానీ పార్టీ! 🍲🤤", "emoji": "🍲", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "NTR Energy", "title": "Lightning Fast Query", "caption": "ఒక్క ఇండెక్స్ తో క్వెరీ స్పీడ్ 100 రెట్లు పెరిగింది.. రచ్చ రంబోలా! ⚡🔥", "emoji": "⚡", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Pawan Kalyan Craze", "title": "Gabbar Singh Review", "caption": "నా రివ్యూ వస్తే కామెంట్స్ ఉండవు.. కేవలం అప్రూవల్సే! 🦁🔥", "emoji": "🦁", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Venkatesh Comedy", "title": "Smooth Release No Tension", "caption": "ఈసారి ఎలాంటి టెన్షన్ లేకుండా ప్రొడక్షన్ రిలీజ్ అయిపోయింది భయ్యా! 🌈😄", "emoji": "🌈", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Relatable Tech", "title": "Bonus Credited Message", "caption": "అకౌంట్ లో బోనస్ క్రెడిట్ అయిందని మెసేజ్ వచ్చింది.. దిమ్మతిరిగి బొమ్మ కనిపించింది! 💸🥳", "emoji": "💸", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Tollywood Punch", "title": "Mass Raja Speed", "caption": "రవితేజ స్పీడ్ లో కోడ్ రాసి టెస్ట్ కేసెస్ అన్ని గ్రీన్ చేశాం! ⚡🏁", "emoji": "⚡", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Pushpa Fire", "title": "Pushpa Raj Victory", "caption": "క్లయింట్ ఇచ్చిన డెడ్‌లైన్ కంటే ముందే ప్రాజెక్ట్ సబ్మిట్ చేసేశాం! 🏆✨", "emoji": "🏆", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Weekend Mood", "title": "Saturday Morning Freedom", "caption": "శనివారం ఉదయం అలారం లేకుండా హాయిగా మేల్కొనే ఆనందం వేరురా బాబు! 🌅🛌", "emoji": "🌅", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Brahmi Dance", "title": "PR Approved Quickly", "caption": "పీఆర్ రైజ్ చేయగానే 2 నిమిషాల్లో అప్రూవ్ అయిపోయింది.. పండగే ఇక! 💃🎊", "emoji": "💃", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Tech Success", "title": "Cloud Migration Done", "caption": "క్లౌడ్ మైగ్రేషన్ లో ఒక్క ఎర్రర్ కూడా రాలేదు.. టీమ్ మొత్తం సంబరాలు! ☁️🎉", "emoji": "☁️", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Salary Bliss", "title": "First Month Salary Joy", "caption": "మొదటి సాలరీ పడగానే అమ్మకి చీర, నాన్నకి వాచ్ కొనిచ్చిన తృప్తి! 🎁❤️", "emoji": "🎁", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Coffee Energy", "title": "Filter Coffee Boost", "caption": "ఉదయాన్నే వేడివేడి డిగ్రీ కాఫీ తాగగానే బ్రెయిన్ సూపర్ ఫాస్ట్ గా పనిచేస్తోంది! ☕🚀", "emoji": "☕", "sentiment": "positive", "slug": "leo"},
    {"lang": "Telugu", "tag": "Code Wizard", "title": "Refactoring Victory", "caption": "వెయ్యి లైన్ల కోడ్ ని వంద లైన్లలో రాసి యాప్ స్పీడ్ డబుల్ చేసేశాను! 🪄💡", "emoji": "🪄", "sentiment": "positive", "slug": "leo"},

    # Neutral (24)
    {"lang": "Telugu", "tag": "Hitec City IT", "title": "Rao Ramesh Philosophy", "caption": "లైఫ్ లో ఏదో సాధిద్దాం అనుకున్నాం.. కానీ రోజూ మీటింగ్స్ తోనే సరిపోతోంది 🥲", "emoji": "🧘", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "BTech Struggles", "title": "One Night Standup Study", "caption": "ఎగ్జామ్ ముందు రోజు రాత్రి: ఈ ఒక్క నైట్ చదివితే యూనివర్సిటీ టాపర్ అయిపోతాను! 📚", "emoji": "📚", "sentiment": "neutral", "slug": "fry"},
    {"lang": "Telugu", "tag": "Traffic Trauma", "title": "Gachibowli Flyover Traffic", "caption": "గచ్చిబౌలి ఫ్లైఓవర్ ట్రాఫిక్ లో కూర్చుని జీవితం మీద వేదాంతం ఆలోచించే క్షణాలు 🚗🛵", "emoji": "🚗", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Code Mystery", "title": "Working Code Don't Touch", "caption": "ఈ లైన్ ఎందుకు రాశానో నాకే తెలియదు, కానీ తీసేస్తే యాప్ మొత్తం క్రాష్ అవుతోంది! 🚫", "emoji": "🚫", "sentiment": "neutral", "slug": "rollsafe"},
    {"lang": "Telugu", "tag": "Family Drama", "title": "Relative Asking Salary", "caption": "చుట్టాలు వచ్చి: బాబు జీతం ఎంత అంటే.. ఇన్ కమ్ టాక్స్ ఆఫీసర్ లా చూస్తున్న వాళ్లు 🤐", "emoji": "🤐", "sentiment": "neutral", "slug": "sarcasticbear"},
    {"lang": "Telugu", "tag": "Corporate Reality", "title": "Daily Standup Update", "caption": "నిన్న ఏం చేశావు అంటే ఆలోచించడానికి ఐదు నిమిషాలు టైమ్ కావాలి మేనేజర్ గారూ ⏳📋", "emoji": "⏳", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Tea Break", "title": "Madhapur Chai Adda", "caption": "కోడ్ లో బగ్ రాలేదు కానీ చాయ్ తాగడానికి ఒక చిన్న కారణం దొరికింది ☕🫖", "emoji": "☕", "sentiment": "neutral", "slug": "kermit"},
    {"lang": "Telugu", "tag": "WFH Habit", "title": "Camera Off Sleeping", "caption": "ఆల్ హ్యాండ్స్ మీటింగ్ లో కెమెరా ఆఫ్ చేసి సైలెంట్ గా కాఫీ తాగుతున్న క్షణాలు ☕🛋️", "emoji": "☕", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Tech Update", "title": "New Framework Released", "caption": "నేను పాత ఫ్రేమ్‌వర్క్ నేర్చుకునేలోపు మార్కెట్ లోకి ఇంకో కొత్తది వచ్చేసింది 🔄💻", "emoji": "🔄", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Commute Story", "title": "Metro Route Routine", "caption": "రాయదుర్గం మెట్రో లో నిలబడి సీట్ కోసం ఎదురుచూసే దినచర్య 🚇🎧", "emoji": "🚇", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Lunch Decision", "title": "Mess Food vs Swiggy", "caption": "మధ్యాహ్నం ఏం తినాలి అని ఆలోచించడానికే ఒక గంట మీటింగ్ పడుతుంది 🍱🤔", "emoji": "🍱", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Weekend Plan", "title": "Saturday Sleep Goal", "caption": "ఈ శనివారం చాలా చదవాలి అనుకున్నాను కానీ మధ్యాహ్నం 12 వరకు నిద్రపోయాను 😴🛌", "emoji": "😴", "sentiment": "neutral", "slug": "cheems"},
    {"lang": "Telugu", "tag": "Documentation", "title": "Empty Readme File", "caption": "ఈ ప్రాజెక్ట్ కి డాక్యుమెంటేషన్ రాయడం అంటే హిమాలయాల్లో తపస్సు చేయడం లాంటిది 📄🏔️", "emoji": "📄", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Weather Talk", "title": "Hyderabad Rain Traffic", "caption": "చిన్న చినుకు పడగానే హైటెక్ సిటీ రోడ్లు చెరువుల్లా మారిపోయే చిత్రం 🌧️🚶‍♂️", "emoji": "🌧️", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Sprint Planning", "title": "Story Point Estimation", "caption": "ఈ టాస్క్ కి 3 పాయింట్లా లేక 5 పాయింట్లా అని అందరూ సీరియస్ గా చర్చలు 🎲📊", "emoji": "🎲", "sentiment": "neutral", "slug": "rollsafe"},
    {"lang": "Telugu", "tag": "Gym Resolution", "title": "Monthly Subscription Reality", "caption": "జిమ్ ఫీజు కట్టేశాం.. కానీ వెళ్లింది మాత్రం మొదటి రోజే 🏋️‍♂️🤷‍♂️", "emoji": "🏋️‍♂️", "sentiment": "neutral", "slug": "cheems"},
    {"lang": "Telugu", "tag": "Desk Setup", "title": "Dual Monitor Workspace", "caption": "ఒక స్క్రీన్ లో కోడ్, ఇంకో స్క్రీన్ లో క్రికెట్ స్కోర్.. ఇదే మన వర్క్ స్టేషన్ 🖥️🏏", "emoji": "🖥️", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Coffee Habit", "title": "Irani Chai Biscuit", "caption": "ఇరానీ చాయ్ లో ఉస్మానియా బిస్కెట్ ముంచి తింటూ కోడ్ ని చూస్తున్నాను ☕🍪", "emoji": "☕", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Meeting Routine", "title": "Mute Button Safety", "caption": "మీటింగ్ లో ఉన్నంతసేపు మ్యూట్ లో ఉన్నానా లేదా అని పదిసార్లు చెక్ చేసుకోవడం 🎙️👀", "emoji": "🎙️", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Git History", "title": "Old Commit Messages", "caption": "రెండేళ్ల క్రితం నేను రాసిన కామెంట్స్ చదివి నాకే అర్థం కావడం లేదు 📜🤔", "emoji": "📜", "sentiment": "neutral", "slug": "rollsafe"},
    {"lang": "Telugu", "tag": "Shopping Cart", "title": "Amazon Wishlist Waiting", "caption": "విష్‌లిస్ట్ లో 20 గ్యాడ్జెట్లు ఉన్నాయి కానీ కొనడానికి జీతం సరిపోదు 🛒💭", "emoji": "🛒", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Online Course", "title": "50 Percent Video Course", "caption": "కోర్సు సగం చూసి ఆపేశాను.. ఎప్పటికైనా మిగతాది పూర్తి చేయాలని ఆశ 💻📚", "emoji": "💻", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Keyboard Typing", "title": "Fast Typing No Output", "caption": "కీబోర్డ్ మీద టకటకమని సౌండ్ వస్తోంది కానీ స్క్రీన్ మీద ఒక్క లైన్ కూడా పడలేదు ⌨️🙃", "emoji": "⌨️", "sentiment": "neutral", "slug": "fine"},
    {"lang": "Telugu", "tag": "Evening Walk", "title": "Durgam Cheruvu Walk", "caption": "దుర్గం చెరువు కేబుల్ బ్రిడ్జ్ మీద చల్లగాలి పీలుస్తూ ఆలోచనల్లో మునిగిపోయాను 🌉🚶‍♂️", "emoji": "🌉", "sentiment": "neutral", "slug": "fine"},

    # Negative (24)
    {"lang": "Telugu", "tag": "Salary Sarcasm", "title": "1st vs 30th Reality", "caption": "జీతం పడ్డ మొదటి రోజు బాహుబలి.. నెల చివరి రోజు భిక్షాటన 💸😭", "emoji": "💸", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Corporate Chaos", "title": "Friday 6 PM Release", "caption": "ఫ్రైడే ఈవెనింగ్ 6 గంటలకు ప్రొడక్షన్ రిలీజ్ ప్లాన్ చేసిన మేనేజర్ ని చూస్తూ నేను 🚨💀", "emoji": "🚨", "sentiment": "negative", "slug": "sarcasticbear"},
    {"lang": "Telugu", "tag": "Client vs Dev", "title": "Sunil Confusion", "caption": "క్లయింట్ చెప్పిన రిక్వైర్మెంట్ vs నేను రాసిన కోడ్.. రెండింటికీ అసలు సంబంధమే లేదు! 🤷‍♂️", "emoji": "🤷‍♂️", "sentiment": "negative", "slug": "drake"},
    {"lang": "Telugu", "tag": "WFH Dilemma", "title": "Camera On Panic", "caption": "మేనేజర్: అందరూ కెమెరా ఆన్ చేయండి! మంచం మీద లుంగీతో పడుకున్న నేను 😱🛏️", "emoji": "😱", "sentiment": "negative", "slug": "ch"},
    {"lang": "Telugu", "tag": "Brahmi Tears", "title": "Merge Conflict Disaster", "caption": "500 ఫైల్స్ లో కాన్ఫ్లిక్ట్ వచ్చింది.. నా చేతులు వణికిపోతున్నాయి భయ్యా! 😭💻", "emoji": "😭", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Prod Outage", "title": "Server Crash At Midnight", "caption": "రాత్రి 2 గంటలకు ఆన్-కాల్ పేజర్ మోగింది.. సర్వర్ మొత్తం డౌన్ అయిపోయింది 🚨💀", "emoji": "🚨", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Appraisal Pain", "title": "1 Percent Hike Agony", "caption": "ఇంత కష్టపడితే ఇచ్చిన హైక్ 1 శాతం.. గుండె పగిలిపోయింది దేవుడా 💔💸", "emoji": "💔", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Interview Failure", "title": "Rejected In Round 4", "caption": "4 రౌండ్స్ అయ్యాక బడ్జెట్ లేదని రిజెక్ట్ చేశారు.. ఇంతకంటే ద్రోహం ఉందా! 😤🚪", "emoji": "😤", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Monday Gloom", "title": "Sunday Night Anxiety", "caption": "ఆదివారం రాత్రి 10 గంటలవగానే సోమవారం ఆఫీస్ గుర్తొచ్చి గుండెల్లో దడ మొదలైంది ⏰😰", "emoji": "😰", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Database Horror", "title": "Drop Table Without Where", "caption": "టెస్ట్ డీబీ అనుకుని ప్రొడక్షన్ డీబీ ని డ్రాప్ చేసేశాను.. కెరీర్ సమాప్తం! 💥😱", "emoji": "💥", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Overtime Burden", "title": "Midnight 3 AM Working", "caption": "అందరూ ప్రశాంతంగా నిద్రపోతుంటే నేను ఇక్కడ బగ్స్ కోసం ఏడుస్తున్నాను 🌙😭", "emoji": "😭", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Internet Loss", "title": "WiFi Cut During Presentation", "caption": "క్లయింట్ కి ప్రజెంటేషన్ ఇస్తుండగా నెట్ పోయింది.. కొంప మునిగిపోయింది! 🔌🛑", "emoji": "🛑", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Loan Stress", "title": "EMI Deduction Message", "caption": "జీతం వచ్చిన వెంటనే EMI కట్ అయిపోయింది.. చేతిలో చిల్లిగవ్వ లేదు 💸📉", "emoji": "📉", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Laptop Dead", "title": "Blue Screen Of Death", "caption": "సేవ్ చేయని ప్రాజెక్ట్ ఉండగా ల్యాప్‌టాప్ బ్లూ స్క్రీన్ ఇచ్చేసింది.. కన్నీళ్లే మిగిలాయి 💻💀", "emoji": "💻", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Toxic Boss", "title": "Micro Management Nightmare", "caption": "ప్రతి అరగంటకి వచ్చి స్టేటస్ అడిగే మేనేజర్ ని తట్టుకోలేకపోతున్నాను భయ్యా 🤬😤", "emoji": "🤬", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Cancelled Leave", "title": "Leave Rejected For Holiday", "caption": "సంక్రాంతి సెలవులకి ప్లాన్ చేసుకుంటే లీవ్ రిజెక్ట్ చేశారు.. ఘోరమైన అన్యాయం 🚷😭", "emoji": "😭", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Bug Nightmare", "title": "Null Pointer Exception Loop", "caption": "వందసార్లు చెక్ చేసినా నల్ పాయింటర్ ఎక్సెప్షన్ పోవడం లేదు.. పిచ్చెక్కుతోంది! 🤯🔥", "emoji": "🤯", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Rent Hike", "title": "Madhapur Rent Shock", "caption": "రూమ్ అద్దె 50 శాతం పెంచేశారు.. ఇక రోడ్డు పక్కన పడుకోవడమే దిక్కు! 💸🏚️", "emoji": "💸", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Broken AC", "title": "Summer Without AC", "caption": "మే నెల ఎండల్లో ఏసీ చెడిపోయింది.. ఉడికిపోతున్నాం భయ్యా! 🥵🔥", "emoji": "🥵", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Food Poison", "title": "Bad Hostel Mess Food", "caption": "హాస్టల్ ఫుడ్ తిని మూడు రోజులుగా కడుపునొప్పితో నరకం చూస్తున్నాను 🤢🏥", "emoji": "🤢", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Stolen Phone", "title": "Lost Phone In Bus", "caption": "బస్సులో ఫోన్ పోయింది.. అందులోనే నా కోడ్, బ్యాంకింగ్ యాప్స్ అన్నీ ఉన్నాయి! 📱😭", "emoji": "😭", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Project Scrapped", "title": "6 Months Work Cancelled", "caption": "ఆరు నెలలు కష్టపడి కట్టిన ప్రాజెక్ట్ ని క్లయింట్ స్క్రాప్ చేసేశాడు.. గుండె పగిలింది 💔🗑️", "emoji": "💔", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Traffic Fine", "title": "Challan On Empty Signal", "caption": "ఖాళీ రోడ్డు మీద కూడా ట్రాఫిక్ చలాన్ పడింది.. జేబు ఖాళీ అయిపోయింది 🚨💸", "emoji": "🚨", "sentiment": "negative", "slug": "bad"},
    {"lang": "Telugu", "tag": "Overload Tasks", "title": "Three Sprints Work In One", "caption": "ముగ్గురి పనిని నా ఒక్కడి నెత్తిన పెట్టేశారు.. ఊపిరి కూడా ఆడనివ్వడం లేదు 😫🧱", "emoji": "😫", "sentiment": "negative", "slug": "bad"},
]

# Write and run the seeding script
