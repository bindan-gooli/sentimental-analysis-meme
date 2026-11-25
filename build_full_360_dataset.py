import os
import sqlite3

DB_PATH = "/Users/bindanm/IndicSent-M/memes.db"

# Master Database with 360 Culturally Authentic, High-Quality Memes
# 5 Languages (Telugu, Bengali, Hindi, Tamil, Global)
# 72 per Language: 24 Positive, 24 Neutral, 24 Negative
# Exactly 120 Positive, 120 Neutral, 120 Negative total

MEMES_DATA = []

# TELUGU (24 Pos, 24 Neu, 24 Neg)
TELUGU_POS = [
    ("First Try Compile Success", "వామ్మో! ఈ కోడ్ ఫస్ట్ అటెంప్ట్‌లోనే రన్ అయింది! 😂🔥", "ch", "Tollywood Punch", "🤯"),
    ("Thaggedhe Le Deployment", "టెస్టింగ్ చేయకుండానే ప్రొడక్షన్ లో డిప్లాయ్ చేశాం.. తగ్గేదే లే! 🪓🔥", "leo", "Pushpa Vibe", "🪓"),
    ("Single Click Bugfix", "సింగిల్ క్లిక్ తో 50 బగ్స్ క్లియర్ చేసి వీకెండ్ బిర్యానీ తింటున్న మూడ్ 🍗😎", "leo", "Balayya Power", "🍗"),
    ("Natu Natu Signoff", "క్లయింట్ సైలెంట్ గా సైన్ ఆఫ్ ఇచ్చేశాడు.. ఇక నాటు నాటు డాన్సే! 🕺🏆", "leo", "RRR Celebration", "🕺"),
    ("Friday Logout Bliss", "శుక్రవారం సాయంత్రం 5 గంటలకు స్లాక్ లో ఆఫ్లైన్ పెట్టే ఆనందం వేరురా బాబు 🎉🍻", "leo", "Weekend Vibe", "🎉"),
    ("Google Copy Paste Win", "ఇంటర్య్వూలో 5 ఇయర్స్ సీనియర్ డెవలపర్ అని చెప్పి.. గూగుల్ లో లూప్ ఎలా రాయాలో వెతుకుతున్న నేను 💻", "rollsafe", "Ali Comedy", "💻"),
    ("Appraisal Letter Received", "అనుకున్నదానికంటే ఎక్కువ హైక్ వచ్చింది.. ఇక పార్టీ టైమ్ రా బాబు! 🥳💰", "leo", "Brahmi Joy", "🥳"),
    ("Clean Code Architecture", "నా కోడ్ చూసి సీనియర్ ఆర్కిటెక్ట్ కూడా ఫిదా అయ్యాడు.. అది నా బ్రాండ్! ✨💼", "leo", "Mahesh Babu Swag", "✨"),
    ("Feature Demo Success", "డెమో లో క్లయింట్ క్లాప్స్ కొట్టాడు.. సూపర్ హిట్ రా మామా! 👏🌟", "leo", "Chiranjeevi Energy", "👏"),
    ("Elegant One Liner Fix", "మాటల్లో ప్రాస, కోడ్ లో లాజిక్.. రెండూ మనకు వెన్నతో పెట్టిన విద్య! 🎯💡", "rollsafe", "Trivikram Dialouge", "🎯"),
    ("Zero Bug Delivery", "స్ప్రింట్ పూర్తయింది, జీరో బగ్స్.. తగ్గేదే లే అసలు! 🚀🏆", "leo", "Allu Arjun Style", "🚀"),
    ("Paradise Biryani Treat", "ప్రాజెక్ట్ డెలివరీ అయిపోయింది.. బావార్చి లో డబుల్ మసాలా బిర్యానీ పార్టీ! 🍲🤤", "leo", "Hyd Biryani", "🍲"),
    ("Lightning Fast Query", "ఒక్క ఇండెక్స్ తో క్వెరీ స్పీడ్ 100 రెట్లు పెరిగింది.. రచ్చ రంబోలా! ⚡🔥", "leo", "NTR Energy", "⚡"),
    ("Gabbar Singh Review", "నా రివ్యూ వస్తే కామెంట్స్ ఉండవు.. కేవలం అప్రూవల్సే! 🦁🔥", "leo", "Pawan Kalyan Craze", "🦁"),
    ("Smooth Release No Tension", "ఈసారి ఎలాంటి టెన్షన్ లేకుండా ప్రొడక్షన్ రిలీజ్ అయిపోయింది భయ్యా! 🌈😄", "leo", "Venkatesh Comedy", "🌈"),
    ("Bonus Credited Message", "అకౌంట్ లో బోనస్ క్రెడిట్ అయిందని మెసేజ్ వచ్చింది.. దిమ్మతిరిగి బొమ్మ కనిపించింది! 💸🥳", "leo", "Relatable Tech", "💸"),
    ("Mass Raja Speed", "రవితేజ స్పీడ్ లో కోడ్ రాసి టెస్ట్ కేసెస్ అన్ని గ్రీన్ చేశాం! ⚡🏁", "leo", "Tollywood Punch", "⚡"),
    ("Pushpa Raj Victory", "క్లయింట్ ఇచ్చిన డెడ్‌లైన్ కంటే ముందే ప్రాజెక్ట్ సబ్మిట్ చేసేశాం! 🏆✨", "leo", "Pushpa Fire", "🏆"),
    ("Saturday Morning Freedom", "శనివారం ఉదయం అలారం లేకుండా హాయిగా మేల్కొనే ఆనందం వేరురా బాబు! 🌅🛌", "leo", "Weekend Mood", "🌅"),
    ("PR Approved Quickly", "పీఆర్ రైజ్ చేయగానే 2 నిమిషాల్లో అప్రూవ్ అయిపోయింది.. పండగే ఇక! 💃🎊", "leo", "Brahmi Dance", "💃"),
    ("Cloud Migration Done", "క్లౌడ్ మైగ్రేషన్ లో ఒక్క ఎర్రర్ కూడా రాలేదు.. టీమ్ మొత్తం సంబరాలు! ☁️🎉", "leo", "Tech Success", "☁️"),
    ("First Month Salary Joy", "మొదటి సాలరీ పడగానే అమ్మకి చీర, నాన్నకి వాచ్ కొనిచ్చిన తృప్తి! 🎁❤️", "leo", "Salary Bliss", "🎁"),
    ("Filter Coffee Boost", "ఉదయాన్నే వేడివేడి డిగ్రీ కాఫీ తాగగానే బ్రెయిన్ సూపర్ ఫాస్ట్ గా పనిచేస్తోంది! ☕🚀", "leo", "Coffee Energy", "☕"),
    ("Refactoring Victory", "వెయ్యి లైన్ల కోడ్ ని వంద లైన్లలో రాసి యాప్ స్పీడ్ డబుల్ చేసేశాను! 🪄💡", "leo", "Code Wizard", "🪄")
]

TELUGU_NEU = [
    ("Rao Ramesh Philosophy", "లైఫ్ లో ఏదో సాధిద్దాం అనుకున్నాం.. కానీ రోజూ మీటింగ్స్ తోనే సరిపోతోంది 🥲", "fine", "Hitec City IT", "🧘"),
    ("One Night Standup Study", "ఎగ్జామ్ ముందు రోజు రాత్రి: ఈ ఒక్క నైట్ చదివితే యూనివర్సిటీ టాపర్ అయిపోతాను! 📚", "fry", "BTech Struggles", "📚"),
    ("Gachibowli Flyover Traffic", "గచ్చిబౌలి ఫ్లైఓవర్ ట్రాఫిక్ లో కూర్చుని జీవితం మీద వేదాంతం ఆలోచించే క్షణాలు 🚗🛵", "fine", "Traffic Trauma", "🚗"),
    ("Working Code Don't Touch", "ఈ లైన్ ఎందుకు రాశానో నాకే తెలియదు, కానీ తీసేస్తే యాప్ మొత్తం క్రాష్ అవుతోంది! 🚫", "rollsafe", "Code Mystery", "🚫"),
    ("Relative Asking Salary", "చుట్టాలు వచ్చి: బాబు జీతం ఎంత అంటే.. ఇన్ కమ్ టాక్స్ ఆఫీసర్ లా చూస్తున్న వాళ్లు 🤐", "sarcasticbear", "Family Drama", "🤐"),
    ("Daily Standup Update", "నిన్న ఏం చేశావు అంటే ఆలోచించడానికి ఐదు నిమిషాలు టైమ్ కావాలి మేనేజర్ గారూ ⏳📋", "fine", "Corporate Reality", "⏳"),
    ("Madhapur Chai Adda", "కోడ్ లో బగ్ రాలేదు కానీ చాయ్ తాగడానికి ఒక చిన్న కారణం దొరికింది ☕🫖", "kermit", "Tea Break", "☕"),
    ("Camera Off Sleeping", "ఆల్ హ్యాండ్స్ మీటింగ్ లో కెమెరా ఆఫ్ చేసి సైలెంట్ గా కాఫీ తాగుతున్న క్షణాలు ☕🛋️", "fine", "WFH Habit", "☕"),
    ("New Framework Released", "నేను పాత ఫ్రేమ్‌వర్క్ నేర్చుకునేలోపు మార్కెట్ లోకి ఇంకో కొత్తది వచ్చేసింది 🔄💻", "fine", "Tech Update", "🔄"),
    ("Metro Route Routine", "రాయదుర్గం మెట్రో లో నిలబడి సీట్ కోసం ఎదురుచూసే దినచర్య 🚇🎧", "fine", "Commute Story", "🚇"),
    ("Mess Food vs Swiggy", "మధ్యాహ్నం ఏం తినాలి అని ఆలోచించడానికే ఒక గంట మీటింగ్ పడుతుంది 🍱🤔", "fine", "Lunch Decision", "🍱"),
    ("Saturday Sleep Goal", "ఈ శనివారం చాలా చదవాలి అనుకున్నాను కానీ మధ్యాహ్నం 12 వరకు నిద్రపోయాను 😴🛌", "cheems", "Weekend Plan", "😴"),
    ("Empty Readme File", "ఈ ప్రాజెక్ట్ కి డాక్యుమెంటేషన్ రాయడం అంటే హిమాలయాల్లో తపస్సు చేయడం లాంటిది 📄🏔️", "fine", "Documentation", "📄"),
    ("Hyderabad Rain Traffic", "చిన్న చినుకు పడగానే హైటెక్ సిటీ రోడ్లు చెరువుల్లా మారిపోయే చిత్రం 🌧️🚶‍♂️", "fine", "Weather Talk", "🌧️"),
    ("Story Point Estimation", "ఈ టాస్క్ కి 3 పాయింట్లా లేక 5 పాయింట్లా అని అందరూ సీరియస్ గా చర్చలు 🎲📊", "rollsafe", "Sprint Planning", "🎲"),
    ("Monthly Subscription Reality", "జిమ్ ఫీజు కట్టేశాం.. కానీ వెళ్లింది మాత్రం మొదటి రోజే 🏋️‍♂️🤷‍♂️", "cheems", "Gym Resolution", "🏋️‍♂️"),
    ("Dual Monitor Workspace", "ఒక స్క్రీన్ లో కోడ్, ఇంకో స్క్రీన్ లో క్రికెట్ స్కోర్.. ఇదే మన వర్క్ స్టేషన్ 🖥️🏏", "fine", "Desk Setup", "🖥️"),
    ("Irani Chai Biscuit", "ఇరానీ చాయ్ లో ఉస్మానియా బిస్కెట్ ముంచి తింటూ కోడ్ ని చూస్తున్నాను ☕🍪", "fine", "Coffee Habit", "☕"),
    ("Mute Button Safety", "మీటింగ్ లో ఉన్నంతసేపు మ్యూట్ లో ఉన్నానా లేదా అని పదిసార్లు చెక్ చేసుకోవడం 🎙️👀", "fine", "Meeting Routine", "🎙️"),
    ("Old Commit Messages", "రెండేళ్ల క్రితం నేను రాసిన కామెంట్స్ చదివి నాకే అర్థం కావడం లేదు 📜🤔", "rollsafe", "Git History", "📜"),
    ("Amazon Wishlist Waiting", "విష్‌లిస్ట్ లో 20 గ్యాడ్జెట్లు ఉన్నాయి కానీ కొనడానికి జీతం సరిపోదు 🛒💭", "fine", "Shopping Cart", "🛒"),
    ("50 Percent Video Course", "కోర్సు సగం చూసి ఆపేశాను.. ఎప్పటికైనా మిగతాది పూర్తి చేయాలని ఆశ 💻📚", "fine", "Online Course", "💻"),
    ("Fast Typing No Output", "కీబోర్డ్ మీద టకటకమని సౌండ్ వస్తోంది కానీ స్క్రీన్ మీద ఒక్క లైన్ కూడా పడలేదు ⌨️🙃", "fine", "Keyboard Typing", "⌨️"),
    ("Durgam Cheruvu Walk", "దుర్గం చెరువు కేబుల్ బ్రిడ్జ్ మీద చల్లగాలి పీలుస్తూ ఆలోచనల్లో మునిగిపోయాను 🌉🚶‍♂️", "fine", "Evening Walk", "🌉")
]

TELUGU_NEG = [
    ("1st vs 30th Reality", "జీతం పడ్డ మొదటి రోజు బాహుబలి.. నెల చివరి రోజు భిక్షాటన 💸😭", "bad", "Salary Sarcasm", "💸"),
    ("Friday 6 PM Release", "ఫ్రైడే ఈవెనింగ్ 6 గంటలకు ప్రొడక్షన్ రిలీజ్ ప్లాన్ చేసిన మేనేజర్ ని చూస్తూ నేను 🚨💀", "sarcasticbear", "Corporate Chaos", "🚨"),
    ("Sunil Confusion", "క్లయింట్ చెప్పిన రిక్వైర్మెంట్ vs నేను రాసిన కోడ్.. రెండింటికీ అసలు సంబంధమే లేదు! 🤷‍♂️", "drake", "Client vs Dev", "🤷‍♂️"),
    ("Camera On Panic", "మేనేజర్: అందరూ కెమెరా ఆన్ చేయండి! మంచం మీద లుంగీతో పడుకున్న నేను 😱🛏️", "ch", "WFH Dilemma", "😱"),
    ("Merge Conflict Disaster", "500 ఫైల్స్ లో కాన్ఫ్లిక్ట్ వచ్చింది.. నా చేతులు వణికిపోతున్నాయి భయ్యా! 😭💻", "bad", "Brahmi Tears", "😭"),
    ("Server Crash At Midnight", "రాత్రి 2 గంటలకు ఆన్-కాల్ పేజర్ మోగింది.. సర్వర్ మొత్తం డౌన్ అయిపోయింది 🚨💀", "bad", "Prod Outage", "🚨"),
    ("1 Percent Hike Agony", "ఇంత కష్టపడితే ఇచ్చిన హైక్ 1 శాతం.. గుండె పగిలిపోయింది దేవుడా 💔💸", "bad", "Appraisal Pain", "💔"),
    ("Rejected In Round 4", "4 రౌండ్స్ అయ్యాక బడ్జెట్ లేదని రిజెక్ట్ చేశారు.. ఇంతకంటే ద్రోహం ఉందా! 😤🚪", "bad", "Interview Failure", "😤"),
    ("Sunday Night Anxiety", "ఆదివారం రాత్రి 10 గంటలవగానే సోమవారం ఆఫీస్ గుర్తొచ్చి గుండెల్లో దడ మొదలైంది ⏰😰", "bad", "Monday Gloom", "😰"),
    ("Drop Table Without Where", "టెస్ట్ డీబీ అనుకుని ప్రొడక్షన్ డీబీ ని డ్రాప్ చేసేశాను.. కెరీర్ సమాప్తం! 💥😱", "bad", "Database Horror", "💥"),
    ("Midnight 3 AM Working", "అందరూ ప్రశాంతంగా నిద్రపోతుంటే నేను ఇక్కడ బగ్స్ కోసం ఏడుస్తున్నాను 🌙😭", "bad", "Overtime Burden", "😭"),
    ("WiFi Cut In Presentation", "క్లయింట్ కి ప్రజెంటేషన్ ఇస్తుండగా నెట్ పోయింది.. కొంప మునిగిపోయింది! 🔌🛑", "bad", "Internet Loss", "🛑"),
    ("EMI Deduction Message", "జీతం వచ్చిన వెంటనే EMI కట్ అయిపోయింది.. చేతిలో చిల్లిగవ్వ లేదు 💸📉", "bad", "Loan Stress", "📉"),
    ("Blue Screen Of Death", "సేవ్ చేయని ప్రాజెక్ట్ ఉండగా ల్యాప్‌టాప్ బ్లూ స్క్రీన్ ఇచ్చేసింది.. కన్నీళ్లే మిగిలాయి 💻💀", "bad", "Laptop Dead", "💻"),
    ("Micro Management Nightmare", "ప్రతి అరగంటకి వచ్చి స్టేటస్ అడిగే మేనేజర్ ని తట్టుకోలేకపోతున్నాను భయ్యా 🤬😤", "bad", "Toxic Boss", "🤬"),
    ("Leave Rejected For Holiday", "సంక్రాంతి సెలవులకి ప్లాన్ చేసుకుంటే లీవ్ రిజెక్ట్ చేశారు.. ఘోరమైన అన్యాయం 🚷😭", "bad", "Cancelled Leave", "😭"),
    ("Null Pointer Loop", "వందసార్లు చెక్ చేసినా నల్ పాయింటర్ ఎక్సెప్షన్ పోవడం లేదు.. పిచ్చెక్కుతోంది! 🤯🔥", "bad", "Bug Nightmare", "🤯"),
    ("Madhapur Rent Shock", "రూమ్ అద్దె 50 శాతం పెంచేశారు.. ఇక రోడ్డు పక్కన పడుకోవడమే దిక్కు! 💸🏚️", "bad", "Rent Hike", "💸"),
    ("Summer Without AC", "మే నెల ఎండల్లో ఏసీ చెడిపోయింది.. ఉడికిపోతున్నాం భయ్యా! 🥵🔥", "bad", "Broken AC", "🥵"),
    ("Bad Hostel Mess Food", "హాస్టల్ ఫుడ్ తిని మూడు రోజులుగా కడుపునొప్పితో నరకం చూస్తున్నాను 🤢🏥", "bad", "Food Poison", "🤢"),
    ("Lost Phone In Bus", "బస్సులో ఫోన్ పోయింది.. అందులోనే నా కోడ్, బ్యాంకింగ్ యాప్స్ అన్నీ ఉన్నాయి! 📱😭", "bad", "Stolen Phone", "😭"),
    ("6 Months Work Cancelled", "ఆరు నెలలు కష్టపడి కట్టిన ప్రాజెక్ట్ ని క్లయింట్ స్క్రాప్ చేసేశాడు.. గుండె పగిలింది 💔🗑️", "bad", "Project Scrapped", "💔"),
    ("Challan On Empty Signal", "ఖాళీ రోడ్డు మీద కూడా ట్రాఫిక్ చలాన్ పడింది.. జేబు ఖాళీ అయిపోయింది 🚨💸", "bad", "Traffic Fine", "🚨"),
    ("Three Sprints In One", "ముగ్గురి పనిని నా ఒక్కడి నెత్తిన పెట్టేశారు.. ఊపిరి కూడా ఆడనివ్వడం లేదు 😫🧱", "bad", "Overload Tasks", "😫")
]

# BENGALI (24 Pos, 24 Neu, 24 Neg)
BENGALI_POS = [
    ("Disaster Girl Prod Test", "দারুণ খেলা হচ্ছে ভাই! প্রোডাকশনে টেস্ট করে দেখি কী হয় 🚀💥", "disastergirl", "MemoSen Classic", "😼"),
    ("Biryani Emotion", "মায়ের হাতের ইলিশ মাছ vs মেসের ঠান্ডা ডাল-ভাত: চরম চোখের জল 🍲💔", "leo", "Food Emotion", "🍲"),
    ("Bhoot In My Repository", "কোড একবারেই রান হয়ে গেল? নিশ্চিত কোথাও বড় একটা ভূত লুকিয়ে আছে! 👻🚫", "rollsafe", "Ghost Code", "👻"),
    ("East Bengal vs Mohun Bagan", "ডার্বি ম্যাচের দিন অফিসে কাজের কথা বললে মার খাবেন ভাই ⚽🔥", "leo", "Football Rivalry", "⚽"),
    ("Durga Pujo Bonus Credited", "পুজোর বোনাস অ্যাকাউন্টে ঢুকতেই কলকাতার রাস্তায় ঢাকের আওয়াজ! 🥁✨", "leo", "Pujo Joy", "🥁"),
    ("Mogojastro Bug Solved", "মগজাস্ত্র ব্যবহার করে ৫ মিনিটের মধ্যে বাগ সমাধান করে ফেললাম! 🔍💡", "leo", "Feluda Brain", "🔍"),
    ("Adda With Old Friends", "কলেজ স্ট্রিট কফি হাউসে বসে গরম কফি আর বন্ধুদের তুমুল আড্ডা! ☕🎉", "leo", "Coffee House", "☕"),
    ("Client Loved The Feature", "ক্লায়েন্ট রিভিউ মিটিংয়ে বলল: অসাধারণ কাজ হয়েছে! মনটা জুড়িয়ে গেল 🌟👏", "leo", "Client Praise", "🌟"),
    ("Friday Evening Phuchka", "শুক্রবার বিকেলে অফিস ছুটি আর পার্ক স্ট্রিটে দাঁড়িয়ে ফুচকা খাওয়া! 🤤🎊", "leo", "Weekend Mood", "🤤"),
    ("Clean Script Celebration", "আমার কোড যেন রবীন্দ্রনাথের কবিতা, প্রতিটি লাইনে নিখুঁত ছন্দ! 📜✨", "leo", "Code Poetry", "📜"),
    ("Rosogolla After Sprint", "স্প্রিন্ট রিলিজ সফল হতেই টিমের জন্য কে সি দাশের রসগোল্লা! 🍯😋", "leo", "Sweets Love", "🍯"),
    ("Approved Annual Leave", "ম্যানেজার দার্জিলিং ট্যুরের ছুটি মঞ্জুর করে দিয়েছে.. জয় মা তারা! 🏔️🚂", "leo", "Darjeeling Trip", "🏔️"),
    ("Expected Promotion Achieved", "অবশেষে কাঙ্ক্ষিত প্রমোশন লেটার হাতে পেলাম.. আজ আনন্দের সীমা নেই! 🏆🥂", "leo", "Hike Joy", "🏆"),
    ("Nolen Gur Season", "শীতের সকালে নলেন গুড়ের সন্দেশ আর কোডিং.. জীবনটা স্বর্গীয়! ❄️🍯", "leo", "Winter Comfort", "❄️"),
    ("Dada Style Comeback", "লর্ডসের ব্যালকনিতে সৌরভ গাঙ্গুলীর মতো জামা উড়িয়ে কামব্যাক করলাম! 🏏🔥", "leo", "Sourav Ganguly", "🏏"),
    ("Zero Crash On Launch", "অ্যাপ স্টোরে লাইভ হলো এবং কোনও ক্র্যাশ রিপোর্ট নেই.. জয় গুরু! 📱🎉", "leo", "App Release", "📱"),
    ("Satyajit Ray Elegance", "সত্যজিৎ রায়ের চলচ্চিত্রের মতো নিখুঁত এবং নান্দনিক ফ্রন্টএন্ড ডিজাইন! 🎬✨", "leo", "Aesthetic Win", "🎬"),
    ("Rabindra Sangeet Peace", "শান্তিনিকেতনের শান্ত পরিবেশ আর সফল প্রজেক্ট সাবমিশন.. পরম তৃপ্তি! 🌸🎶", "leo", "Cultural Bliss", "🌸"),
    ("Mishti Doi Treat", "টিম মেম্বারদের জন্য নবদ্বীপে তৈরি আসল লাল মিষ্টি দইয়ের ভোজ! 🏺🍮", "leo", "Food Joy", "🏺"),
    ("Flawless Cloud Pipeline", "সিআই-সিডি পাইপলাইন পুরোপুরি সবুজ.. আজ রাতে নিশ্চিন্ত ঘুম! 🟢✅", "leo", "DevOps Win", "🟢"),
    ("Shantiniketan Winter Trip", "পৌষ মেলায় ঘুরতে যাওয়ার টিকিট কনফার্ম হয়ে গেল.. দারুণ আনন্দ! 🎪🚂", "leo", "Winter Festival", "🎪"),
    ("Appreciation Mail", "ডিরেক্টর নিজে ইমেল করে বললেন: আপনার অবদান অবিস্মরণীয়! 💌🌟", "leo", "Executive Praise", "💌"),
    ("Code Optimized 10x", "ডেটাবেস কুয়েরি টিউন করে রেসপন্স টাইম ১০ গুণ বাড়িয়ে দিলাম! ⚡💻", "leo", "Speed Upgrade", "⚡"),
    ("Kolkata Winter Morning", "কুয়াশা ঘেরা ময়দানে ঘোড়দৌড় দেখা আর ভাড়ের গরম চা.. অতুলনীয় সুখ! 🐎☕", "leo", "Kolkata Classic", "🐎")
]

BENGALI_NEU = [
    ("Coffee House Intellectuals", "চা এর দোকানে বসে পুরো বিশ্বের অর্থনীতি আর রাজনীতি সমাধান করে ফেলেছি ☕📰", "kermit", "Kolkata Adda", "☕"),
    ("Topshe Mystery", "তোপসে, এই বাগটার পেছনে নির্ঘাত ম্যানেজারের কোনো গোপন ষড়যন্ত্র আছে! 🔍🧐", "rollsafe", "Feluda Deduction", "🔍"),
    ("Client Deadline Ignored", "ক্লায়েন্ট বলে দিল: কাল সকাল ৯টায় সব চাই! আমি: ঠিক আছে, ঘুম থেকে উঠে ভাবব 😴", "cheems", "Sleep Priority", "😴"),
    ("Byomkesh Truth", "সত্যের সন্ধানে বের হয়ে দেখি পুরো কোডবেসটাই চ্যাটজিপিটি দিয়ে লেখা 🕵️‍♂️💀", "fry", "Bengali Sarcasm", "🕵️‍♂️"),
    ("Khichuri Weather Kolkata", "বৃষ্টির দিনে অফিসে বসে খিচুড়ি আর তেলেভাজার কথা ভাবার সময় 🌧️🍲", "fine", "Rainy Day", "🌧️"),
    ("Esplanade Metro Line", "এসপ্ল্যানেড মেট্রো স্টেশনে দাঁড়িয়ে দার্শনিক চিন্তা করার দৈনিক অভ্যাস 🚇💭", "fine", "Metro Commute", "🚇"),
    ("Salt Lake Sector 5 Bus", "সেক্টর ফাইভের বাসে ঝুলতে ঝুলতে জীবনের মোক্ষলাভের চেষ্টা 🚌🧘", "fine", "Daily Routine", "🚌"),
    ("Boimela Stroll", "বইমেলায় গিয়ে বই কেনার চেয়ে লিটল ম্যাগাজিনের স্টলে চা খাওয়া বেশি জরুরি 📚☕", "fine", "Book Fair", "📚"),
    ("Presidency Canteen Gossip", "ক্যান্টিনে বসে ঘণ্টার পর ঘণ্টা তর্ক করেও কোনও সিদ্ধান্ত বের হলো না 🗣️⏳", "fine", "College Life", "🗣️"),
    ("Mac vs Linux Argument", "উইন্ডোজ বনাম লিনাক্স নিয়ে ক্যাবিনে এক ঘণ্টা ধরে বুদ্ধিজীবী বিতর্ক 💻🐧", "fine", "Tech Debate", "💻"),
    ("Bhaat Ghoom Tradition", "রবিবার দুপুরে মাংস-ভাত খাওয়ার পর একটা দীর্ঘ ভাতঘুমের প্রয়োজনীয়তা 🍛😴", "fine", "Sunday Lazy", "🍛"),
    ("Nothing New In Scrum", "কাল যা বলেছিলাম আজও তাই বলব.. শুধু তারিখটা পাল্টে দিয়েছি 📋🔄", "fine", "Standup Update", "📋"),
    ("Bajar Dor Bargain", "মাছের বাজারে গিয়ে ইলিশের দাম শুনে নীরব দর্শকের ভূমিকা পালন করলাম 🐟👀", "fine", "Market Visit", "🐟"),
    ("Nabobarsho Promises", "পয়লা বৈশাখে বলেছিলাম রোজ সকালে হাঁটব.. এখনও বিছানায় বসে চা খাচ্ছি 🌅🛏️", "cheems", "New Year Goal", "🌅"),
    ("Rabindrasangeet On Loop", "কোড লিখতে বসে ব্যাকগ্রাউন্ডে রবিঠাকুরের গান চালিয়ে দেওয়া এক অদ্ভুত শান্তি 🎵🎧", "fine", "Music Taste", "🎵"),
    ("Winter In June Office", "বাইরে ৪২ ডিগ্রি গরম কিন্তু অফিসের এসির ঠান্ডায় কাশ্মীর মনে হচ্ছে ❄️🏢", "fine", "Office AC", "❄️"),
    ("Howrah Bridge Traffic", "হাওড়া ব্রিজের জ্যামে বসে গঙ্গার জলের দিকে তাকিয়ে ভাবছি জীবনটা কী 🌉💭", "fine", "Traffic Musings", "🌉"),
    ("Tram Line Nostalgia", "গড়িয়াহাট ট্রামে চড়ে ধীরে ধীরে অফিস যাওয়ার পুরনো আমেজ 🚋🕰️", "fine", "Old Calcutta", "🚋"),
    ("Documentation Reading", "লাইব্রেরির ডক্যুমেন্টেশন পড়তে গিয়ে পুরোনো ইতিহাস বই পড়ার অনুভূতি 📜👓", "fine", "Tech Study", "📜"),
    ("Canteen Cutlet Debate", "মিষ্টি মুখ করার আগে চিকেন কাটলেট খাওয়া উচিত কিনা তা নিয়ে গভীর ভাবনা 🍗🍽️", "fine", "Food Debate", "🍗"),
    ("Slack Notification Mute", "সকাল থেকে স্ল্যাকের নোটিফিকেশন সাইলেন্ট করে কোড পর্যবেক্ষণ করছি 🔕👀", "fine", "Quiet Hours", "🔕"),
    ("Evening Gariahat Walk", "দক্ষিণ কলকাতার ফুটপাথে হাঁটার সময় পুরনো বইয়ের গন্ধ খোঁজা 🛍️📖", "fine", "City Walk", "🛍️"),
    ("Monsoon Cloud Watching", "জানলার ধারে বসে বর্ষার মেঘ দেখতে দেখতে মিটিংয়ের সময় পার হয়ে গেল ☁️🪟", "fine", "Daydreaming", "☁️"),
    ("Quarterly Goal Review", "বছরের কোয়ার্টারলি গোল শিটে কী লিখব তা ভেবে খাতা সাদা রেখে দিলাম 📝🤷‍♂️", "fine", "Goal Setting", "📝")
]

BENGALI_NEG = [
    ("Monday Blues Kolkata", "সোমবারে অফিসে যাওয়ার চেয়ে সুন্দরবনে বাঘের সামনে যাওয়া অনেক ভালো ছিল 🐅", "bad", "Corporate Tragedy", "🐅"),
    ("Sector 5 Auto Struggle", "সল্টলেক সেক্টর ৫ এর অটো লাইনে দাঁড়িয়ে মোক্ষ লাভ করার অনুভূতি 🚖🤦‍♂️", "fine", "Salt Lake IT", "🚖"),
    ("Pujo Shopping Budget Crash", "পুজোর শপিং করতে গিয়ে নিজের ব্যাঙ্ক ব্যালেন্স দেখে হার্ট অ্যাটাক 💸😱", "sarcasticbear", "Durga Puja Mood", "💸"),
    ("Semester Exam Night", "সারা বছর পড়া নেই, পরীক্ষার আগের রাতে সিলেবাস দেখে মনে হচ্ছে নতুন গ্রহের ভাষা 📚😭", "fry", "College Life", "😭"),
    ("Database Dropped By Intern", "ইন্টার্ন প্রডাকশন ডাটাবেস ড্রপ করে বাড়ি চলে গেছে.. হায় ভগবান! 😱💥", "bad", "Prod Outage", "😱"),
    ("Peanuts Hike In Appraisal", "সারা বছর গাধার মতো খেটে হাইকের নামে হাতে বাদাম ধরিয়ে দিল! 🥜😭", "bad", "Appraisal Grief", "😭"),
    ("Sealdah Local Stuck In Signal", "শিয়ালদহ লোকাল সিগন্যালে দাঁড়িয়ে ১ ঘণ্টা.. জীবনের প্রতি তীব্র বিরক্তি 🚂🛑", "bad", "Train Delay", "🛑"),
    ("Load Shedding In Summer Night", "কালবৈশাখী এলো না কিন্তু লোডশেডিং এসে রাতের ঘুম কেড়ে নিল 🕯️🥵", "bad", "Hot Summer", "🥵"),
    ("Entire Branch Corrupted", "গিট ব্রাঞ্চে এমন কনফ্লিক্ট হয়েছে যে পুরো প্রজেক্টটাই ডিলিট করতে ইচ্ছে করছে 💻💀", "bad", "Merge Conflict", "💻"),
    ("Angry Escalation Email", "সকাল ১০টায় ক্লায়েন্টের রেড-ফ্ল্যাগ এসকেলেশন ইমেল দেখে রক্তচাপ বেড়ে গেল 🚨📧", "bad", "Client Rage", "🚨"),
    ("Sunday Support Call", "রবিবার সকালে ম্যানেজার ফোন করে বলল: একটু লগইন করতে হবে ভাই! 📞💀", "bad", "Weekend Ruined", "📞"),
    ("Spilled Tea On Keyboard", "কাজের মাঝে কিবোর্ডের ওপর গরম চা ঢেলে ফেললাম.. সব শেষ! ☕💻", "bad", "Broken Laptop", "☕"),
    ("Ghosted After 5 Rounds", "পাঁচ রাউন্ড ইন্টারভিউ নেওয়ার পর কোম্পানি আর কোনও রিপ্লাই দিল না 👻🚪", "bad", "Interview Reject", "👻"),
    ("Kolkata Waterlogging Nightmare", "অফিস থেকে বাড়ি ফেরার পথে কোমর সমান জলে দাঁড়িয়ে কান্না পাচ্ছে 🌧️🚶‍♂️", "bad", "Waterlogging", "🌧️"),
    ("Friday Night 500 Error", "শুক্রবার রাতে ৫টি সার্ভারে ইন্টারনাল সার্ভার এরর.. মাথায় হাত! 🤦‍♂️🚨", "bad", "Failed Deploy", "🤦‍♂️"),
    ("Rent And EMI Devastation", "বাড়িভাড়া আর ইএমআই দিতেই মাসের ৫ তারিখে ওয়ালেট খালি হয়ে গেল 💸📉", "bad", "Salary Vanished", "💸"),
    ("Hostel Food Nightmare", "মেসের খাবারে আবার তেলাপোকা পাওয়া গেছে.. খাওয়া মাথায় উঠল! 🪳🤮", "bad", "Food Poisoning", "🪳"),
    ("Production Memory Leak", "সার্ভারের র‍্যাম ১০০% হয়ে সিস্টেম ক্র্যাশ.. রাতারাতি সব শেষ! 📉💥", "bad", "Out of Memory", "📉"),
    ("Cancelled Puja Vacation", "পুজোর চার দিনই অন-কল সাপোর্ট ডিউটি দিয়েছে ম্যানেজার.. জীবনটাই ব্যর্থ! 🚷💔", "bad", "Vacation Denied", "🚷"),
    ("Hard Drive Crash No Backup", "হার্ডডিস্ক ক্র্যাশ করে ৩ মাসের গবেষণার ডেটা মুছে গেল.. মাথায় বাজ পড়ল! 💾😭", "bad", "Data Loss", "💾"),
    ("Kolkata Traffic Hell", "মা উড়ালপুলে গাড়ির জ্যামে আটকে থেকে ফ্লাইটের সময় পার হয়ে গেল ✈️🚗", "bad", "Missed Flight", "✈️"),
    ("Salary Deducted For Sick Leave", "অসুস্থ হয়ে একদিন কামাই করায় পুরো দিনের বেতন কেটে নিল কোম্পানি! 🤒💸", "bad", "Unfair Deduction", "🤒"),
    ("Security Exploit Detected", "প্রোডাকশন এপিআই হ্যাক হয়ে সমস্ত ইউজারের ডেটা লিক.. পুলিশ কেস! 🚨🔓", "bad", "Data Breach", "🚨"),
    ("Severe Migraine In Shift", "১২ ঘণ্টা টানা স্ক্রিনে তাকিয়ে অসহ্য মাইগ্রেনের যন্ত্রণায় চোখ খুলতে পারছি না 🤕💻", "bad", "Physical Toll", "🤕")
]

# HINDI (24 Pos, 24 Neu, 24 Neg)
HINDI_POS = [
    ("Munna Bhaiya Royalty", "जब कोड पहली बार में बिना किसी एरर के कंपाइल हो जाए: कभी कभी लगता है अपुन ही भगवान है! 👑🔥", "leo", "Mirzapur Attitude", "👑"),
    ("Faizal Badla", "बाप का, दादा का, भाई का.. सबका बदला लेगा तेरा ये सेमीकोलन 🔫🤠", "bad", "Gangs of Wasseypur", "🔫"),
    ("Formal Top Pyjama Bottom", "कुर्ता ऊपर, पायजामा नीचे: जूम कॉल पर वर्क फ्रॉम होम की असली कहानी 👔🩳", "cheems", "WFH Reality", "👔"),
    ("Profitable Sprint Launch", "भाई तूने तो आग लगा दी! पूरा फीचर बिना बग के रिलीज हो गया 🚀🔥", "leo", "Shark Tank Ashneer", "🚀"),
    ("Salary Credited SMS Joy", "पैसा ही पैसा होगा! जब महीने की पहली तारीख को सैलरी अकाउंट में आ जाए 💰🕺", "leo", "Hera Pheri", "💰"),
    ("Jaadu Ki Jhappi Bugfix", "सीनियर ने एक लाइन में बग ठीक कर दिया.. जादू की झप्पी का अहसास! 🤗✨", "leo", "Munna Bhai MBBS", "🤗"),
    ("Jai Veeru Partnership", "ये दोस्ती हम नहीं तोड़ेंगे: डेवलपर और क्यूए जब मिलकर प्रोडक्शन बचा लें 🤝🎉", "leo", "Sholay Classic", "🤝"),
    ("Sprint 70 Minutes Speech", "ये सत्तर मिनट तुमसे कोई नहीं छीन सकता.. शानदार कोड डिलीवर हो गया! 🏆🌟", "leo", "Chak De India", "🏆"),
    ("Friday Logout Excitement", "शुक्रवार शाम को लैपटॉप बंद करके पार्टी मोड ऑन करने का सुकून! 🍻🎊", "leo", "Golmaal Fun", "🍻"),
    ("Shah Rukh Khan Pose", "जब क्लाइंट बोले 'अप्रूव्ड विद नो चेंजेस': अपनी तो जैसे तैसे कट जाएगी! 😎✨", "leo", "Bollywood Energy", "😎"),
    ("Tapri Chai Post Deployment", "सफल डिप्लॉयमेंट के बाद टपरी पर अदरक वाली चाय और समोसा.. जन्नत! ☕🤤", "leo", "Chai Love", "☕"),
    ("Cricket Match Victory", "मैनेजर ने टीम को दिया पूरा दिन ऑफ.. मैच जीत गए भाई! 🏏🎉", "leo", "Lagaan Spirit", "🏏"),
    ("Main Jhukega Nahi Release", "बग कितना भी गहरा हो, अपुन झुकेगा नहीं साला! 🪓🔥", "leo", "Pushpa Hindi", "🪓"),
    ("Beer Party Phulera", "सचिव जी ने टंकी पर बैठकर बीयर पी ली.. वीकेंड का स्वागत! 🍺🌾", "leo", "Panchayat Sachiv", "🍺"),
    ("All Is Well Deployment", "दिल को बोलो ऑल इज वेल, कोड अपने आप टेस्ट पास कर लेगा! 💖💡", "rollsafe", "Rancho 3 Idiots", "💖"),
    ("Cash Bonus Sweet Box", "दिवाली पर सोनपापड़ी नहीं बल्कि रियल कैश बोनस मिला.. खुशी का ठिकाना नहीं! 🎁🥳", "leo", "Diwali Bonus", "🎁"),
    ("Singham Roar", "आता माझी सटकली बोलकर 10 मिनट में सारे पेंडिंग टिकट्स बंद कर दिए! 🦁🔥", "leo", "Singham Power", "🦁"),
    ("Taare Zameen Par Care", "सीनियर ने प्यार से कोड समझाया और मेंटरशिप दी.. दिल खुश हो गया! 🎨❤️", "leo", "Great Mentorship", "🎨"),
    ("KGF Rocky Bhai Swag", "वायलेंस वायलेंस वायलेंस.. लेकिन हमारा कोड तो केवल वायलिन की तरह बजता है! 🎻✨", "leo", "KGF Style", "🎻"),
    ("Dangal Gold Medal", "म्हारी छोरियां छोरों से कम हैं के: महिला डेवलपर्स ने हैकथॉन जीत लिया! 🥇🏆", "leo", "Dangal Spirit", "🥇"),
    ("Sunday Chole Bhature", "रविवार की सुबह गरमागरम छोले भटूरे और लस्सी.. जीवन का असली आनंद! 🥪🥤", "leo", "Delhi Food", "🥪"),
    ("Client 5 Star Review", "क्लाइंट ने अपवर्क पर 5-स्टार रिव्यू और भारी टिप दे दी! 🌟💸", "leo", "Freelance Win", "🌟"),
    ("Fast Docker Build", "डॉकराइज्ड इमेज 30 सेकंड में बिल्ड हो गई.. एकदम मक्खन! 🐳🚀", "leo", "Docker Speed", "🐳"),
    ("Remote Mountain Work", "हिमाचल की वादियों में बैठकर लैपटॉप पर काम करने का स्वर्ग जैसा नजारा! 🏔️💻", "leo", "Workation Joy", "🏔️")
]

HINDI_NEU = [
    ("Doglapan Exposed", "ये सब दोगलापन है! जब मैनेजमेंट बोलता है वर्क-लाइफ बैलेंस बहुत ज़रूरी है 🤡", "sarcasticbear", "Shark Tank Ashneer", "🤡"),
    ("21 Din Mein Paisa Double", "21 दिन में पूरा प्रॉडक्ट तैयार कर देंगे: सेल्स टीम क्लाइंट से वादा करते हुए 🤥📦", "rollsafe", "Hera Pheri Akshay", "🤥"),
    ("Sundar Problem", "चाय पीते ही क्लाइंट का पैनिक कॉल आ गया.. अब जिंदगी में बस बबिता जी की शांति चाहिए ☕🤦‍♂️", "fine", "TMKOC Jethalal", "☕"),
    ("Raju Ki Maa", "पनीर तो बेटा कुछ दिनों में सुनार की दुकान पर मिलेगा: मंहगाई और अप्रैज़ल का दर्द 🧀💍", "sarcasticbear", "3 Idiots", "🧀"),
    ("Gym & Alarm Reality", "सोमवार की सुबह: आज से रोज 6 बजे उठूंगा! मंगलवार सुबह: अलार्म सीधा डिलीट 😴🛌", "fry", "Monday Alarm", "😴"),
    ("Synergy And Bandwidth", "मीटिंग में 'सिनर्जी' और 'बैंडविड्थ' बोलकर आधा घंटा आराम से निकाल दिया 🗣️📊", "fine", "Corporate Talk", "🗣️"),
    ("Pradhan Ji Discussion", "प्रधान जी पंचायत में बैठकर सोच रहे हैं कि ये ब्लॉकचेन किस चिड़िया का नाम है 🌾🤔", "fine", "Panchayat Pradhan", "🌾"),
    ("Silk Board Jam Philosophy", "सिल्क बोर्ड जाम में बैठे-बैठे मैंने जीवन का सारा दर्शन समझ लिया 🚗🧘", "fine", "Bangalore Traffic", "🚗"),
    ("Salad vs Chole Bhature", "डाइट शुरू की थी लेकिन लंच में छोले भटूरे देखकर मन पिघल गया 🥗🥪", "fine", "Diet Plan", "🥗"),
    ("Nodding On Zoom Call", "जूम कॉल पर सिर्फ सिर हिलाते रहो ताकि लगे कि बहुत ध्यान से सुन रहे हो 💻🙃", "fine", "Remote Work", "💻"),
    ("Checking Score In Meeting", "मैनेजर जब स्क्रीन शेयर कर रहा हो, तब टैब स्विच करके क्रिकेट स्कोर देखना 🏏👀", "rollsafe", "Cricket Score", "🏏"),
    ("Standup Blockers Check", "कोई ब्लॉकर नहीं है लेकिन फिर भी काम कल ही होगा 📋⏳", "fine", "Scrum Master", "📋"),
    ("Agree Agree Influencer", "लिंक्डइन पर ज्ञान बांटने वाले इन्फ्लुएंसर्स को देखकर मौन धारण कर लिया 📱🤐", "fine", "LinkedIn Post", "📱"),
    ("Cart Full No Checkout", "अमेज़न कार्ट में 50 सामान जोड़ लिए पर पेमेंट करने की हिम्मत नहीं हुई 🛒💭", "fine", "Online Shopping", "🛒"),
    ("Binge Watch Netflix", "पूरा वीकेंड कंबल में बैठकर वेब सीरीज देखने का साधारण कार्यक्रम 📺🍿", "fine", "Weekend Routine", "📺"),
    ("Pizza In Office Cafeteria", "ऑफिस में मुफ्त का पिज्जा मिला है तो स्टैंडअप थोड़ा देर से भी चलेगा 🍕😋", "fine", "Casual Friday", "🍕"),
    ("Metro Token Queue", "दिल्ली मेट्रो की लंबी लाइन में टोकन लेने के लिए खड़े होकर समय बिताना 🚇🪙", "fine", "Delhi Metro", "🚇"),
    ("Office Water Cooler", "वॉटर कूलर के पास खड़े होकर शहर के मौसम और ट्रैफिक पर निष्पक्ष चर्चा 🥤🗣️", "fine", "Water Cooler Chat", "🥤"),
    ("Weekend Grocery List", "शनिवार की शाम सब्जी मंडी जाकर धनिया-मिर्ची मुफ्त मांगने की रस्म 🥦🛍️", "fine", "Sabzi Mandi", "🥦"),
    ("Earphones Untangling", "पॉकेट से ईयरफोन निकालकर 10 मिनट तक उसकी उलझन सुलझाने की मशक्कत 🎧🪢", "fine", "Daily Struggle", "🎧"),
    ("Weather Forecast Check", "मौसम विभाग ने बारिश कही थी और बाहर धूप से पसीने छूट रहे हैं ☀️🌦️", "fine", "Weather App", "☀️"),
    ("Screen Time Report", "फोन ने संडे को रिपोर्ट दी: आपका स्क्रीन टाइम 9 घंटे रहा.. तटस्थ स्वीकृति 📱📊", "fine", "Digital Wellbeing", "📱"),
    ("Cafe WiFi Password", "कैफे में जाकर सबसे पहले काउंटर वाले से वाई-फाई का पासवर्ड पूछना 📶☕", "fine", "Cafe Culture", "📶"),
    ("Resume Formatting", "रिज्यूमे में फॉन्ट साइज 10 करें या 11, इसी पर 2 घंटे मंथन 📄🧐", "fine", "Resume Tweak", "📄")
]

HINDI_NEG = [
    ("Baburao Deep Prayer", "उठा ले रे देवा उठा ले.. मेरे को नहीं इस बग को उठा ले! 😭🙏", "bad", "Hera Pheri", "🙏"),
    ("Binod Live Observation", "देख रहे हो बिनोद.. कैसे फ्राइडे शाम 6 बजे नया फीचर डिप्लॉय हो रहा है 💀👀", "drake", "Panchayat Satire", "👀"),
    ("Salary Hike Meeting", "ये कोई तरीका है भीख मांगने का? सैलरी हाइक डिस्कशन में एचआर से मैं 💸", "fry", "Corporate Hike", "💸"),
    ("Missing Semicolon 4 Hours", "बग ढूंढने के लिए पूरा कोड रीराइट कर दिया, फिर पता चला सेमीकोलन मिसिंग था 🤦‍♂️💀", "fine", "Developer Agony", "🤦‍♂️"),
    ("Bro Pushed Straight to Main", "Bro really thought he could fix production without taking a database backup 💀", "cheems", "Code-Mixed Hinglish", "💀"),
    ("Critical Server Down Alert", "रात 3 बजे सर्वर क्रैश हो गया.. पूरी रात जागकर बग ढूंढने की सजा 🚨😭", "bad", "Production Outage", "🚨"),
    ("Peanuts Rating Letter", "साल भर 14 घंटे काम किया और रेटिंग मिली 'मीट्स एक्सपेक्टेशन'.. दिल टूट गया 💔📉", "bad", "Hike Disappointment", "💔"),
    ("Live Coding Panic Attack", "इंटरव्यूअर ने बोला स्क्रीन शेयर करो और मेरा दिमाग बिल्कुल खाली हो गया 🥶😱", "bad", "Interview Agony", "🥶"),
    ("Angry Weekend Call", "शनिवार की सुबह क्लाइंट का गुस्सा भरा कॉल आ गया.. वीकेंड तबाह! 🤬📱", "bad", "Client Rage", "🤬"),
    ("CI CD Pipeline Red", "पूरी पाइपलाइन लाल हो गई.. 20 टेस्ट फेल और प्रोडक्शन ब्लॉक! 🛑💥", "bad", "Broken Build", "🛑"),
    ("Late Night Slack Message", "रात 11 बजे मैनेजर का मैसेज आया: 'क्विक कॉल?'.. पसीना छूट गया 😨💬", "bad", "Toxic Boss", "😨"),
    ("16 Hours Daily Work", "बिना किसी ओवर-टाइम पे के लगातार तीसरे हफ्ते 16 घंटे काम चल रहा है 😫💼", "bad", "Unpaid Overtime", "😫"),
    ("Accidental Git Reset Hard", "गलती से 'git reset --hard' चला दिया और 3 दिन की मेहनत पानी में बह गई 😭💻", "bad", "Data Loss", "😭"),
    ("Bangalore Flat Rent Hike", "मकान मालिक ने 40% किराया बढ़ा दिया.. अब सड़क पर तंबू लगाना पड़ेगा 💸🏚️", "bad", "Rent Burden", "💸"),
    ("Monday Morning 9 AM Meeting", "सोमवार सुबह 9 बजे पहला ही कॉल रिव्यू का.. जिंदगी से भरोसा उठ गया 💀⏰", "bad", "Monday Horror", "💀"),
    ("Standard Auto Reject", "'वी विश यू लक इन योर फ्यूचर एंडेवर्स'.. यह ईमेल पढ़कर आंखों में आंसू आ गए ✉️😢", "bad", "Rejection Mail", "✉️"),
    ("Production Drop Table", "प्रोडक्शन डेटाबेस पर बिना बैकअप के स्क्रिप्ट रन हो गई.. करियर खत्म! 💥😱", "bad", "DB Disaster", "💥"),
    ("Blue Screen Laptop Crash", "बिना सेव किए 4 घंटे का कोड लिखा था और विंडोज ने ब्लू स्क्रीन फेंक दी 💻💀", "bad", "OS Crash", "💻"),
    ("Security Vulnerability Audit", "ऑडिट टीम ने 50 क्रिटिकल सिक्यूरिटी वल्नरेबिलिटी निकाल दीं.. नींद हराम! 🛑🔓", "bad", "Audit Nightmare", "🛑"),
    ("Zero Merits Increment", "कंपनी ने भारी मुनाफा कमाया लेकिन कर्मचारियों को 0% इन्क्रीमेंट दिया 💔📉", "bad", "Corporate Greed", "💔"),
    ("Horrible Food Poisoning", "सस्ते ढाबे का खाना खाकर 3 दिन से ग्लूकोज की बोतल चढ़ रही है 🤢🏥", "bad", "Illness Trauma", "🤢"),
    ("Traffic Jam Missed Train", "ट्रैफिक में फंसने से दिवाली की घर जाने वाली ट्रेन छूट गई.. प्लेटफार्म पर रोना 🚂😭", "bad", "Missed Train", "🚂"),
    ("Laptop Screen Shattered", "बैग जमीन पर गिरते ही मैकबुक की स्क्रीन के दो टुकड़े हो गए 💻💔", "bad", "Hardware Broken", "💻"),
    ("Cancelled Leave On Festival", "होली की छुट्टी पर घर जाने के लिए टिकट बुक की थी और मैनेजर ने मना कर दिया 🎨🚫", "bad", "Holiday Cancelled", "🚫")
]

# TAMIL (24 Pos, 24 Neu, 24 Neg)
TAMIL_POS = [
    ("Mystery Working Script", "கோட் வேலை செய்யுது ஆனா எப்படி செய்யுதுன்னு எனக்கே தெரியல! அஸ்ஸலாமு அலைக்கும் 🤷‍♂️✨", "rollsafe", "Code Magic", "🤷‍♂️"),
    ("Overtime Work Rejection", "மேனேజర్: இன்னைக்கு கொஞ்சம் லேட்டா போக முடியுமா? நான்: வாய்ப்பில்லை ராஜா! 🙅‍♂️🚀", "leo", "Santhanam Counter", "🙅‍♂️"),
    ("Kabali Comeback", "கபாலி டா! பக் எல்லாம் முடிச்சுட்டு புரொடக்ஷன்ல சிங்கம் மாதிரி நிக்கிறோம் 😎🔥", "leo", "Rajinikanth Style", "🦁"),
    ("Master Sprint Complete", "ஸ்பிரிண்ட் வெற்றிகரமாக முடிந்தது.. வாத்தி கம்மிங் கொண்டாட்டம் தான்! 🎵🕺", "leo", "Vijay Thalapathy", "🎵"),
    ("Billa Cool Head", "எவ்வளவு பிரஷர் வந்தாலும் கூலா கோட் பண்ணி பாஸ் பண்ணியாச்சு! 🕶️⚡", "leo", "Ajith Thala", "🕶️"),
    ("Winner Celebration", "கைப்புள்ள ஜெயிச்சுட்டான்டா! கிளைன்ட் முழுசா அப்ரூவல் கொடுத்தாச்சு 🏆🥳", "leo", "Vadivelu Comedy", "🏆"),
    ("Degree Coffee Happiness", "டிகிரி காபிய குடிச்சிட்டு கோட் அடிச்சா பக் தானா ஓடிப்போய்டும்! ☕✨", "leo", "Chennai Filter Coffee", "☕"),
    ("Marina Beach Breeze", "வெள்ளிக்கிழமை சாயங்காலம் மெரினா பீச்ல சுண்டல் சாப்பிடும் ஆனந்தம்! 🏖️🎉", "leo", "Weekend Mood", "🏖️"),
    ("Double Digit Appraisal", "எதிர்பார்க்காத அளவுக்கு அப்ரைசல் வந்திருக்கு.. இன்னைக்கு பிரியாணி விருந்து! 🍗💰", "leo", "Hike Surprise", "🍗"),
    ("Zero Warning Compile", "ஜீரோ வார்னிங், ஜீரோ எரர்.. கம்ப்யூட்டரே கைதட்டுது! 👏💡", "leo", "Clean Architecture", "👏"),
    ("VIP Raghuvaran Win", "வேலையில்லா பட்டதாரி இல்லடா.. இப்போ நான் சீனியர் டெக் லீட்! 👔🌟", "leo", "Dhanush Swag", "👔"),
    ("Ulaga Nayagan Logic", "கமல் சார் படம் மாதிரி என் கோட்ல அவ்வளவு நுணுக்கம் இருக்கு! 🎭🎬", "leo", "Kamal Haasan", "🎭"),
    ("Pongal Leave Sanctioned", "பொங்கல் லீவ் அப்ரூவ் ஆயிடுச்சு.. ஊருக்கு போறோம் ஜாலியா! 🌾🚂", "leo", "Leave Approved", "🌾"),
    ("Happy Demo Meeting", "டெமோ முடிஞ்சதும் கிளைன்ட் பாராட்டு மழை பொழிஞ்சுட்டான்! 🌟🤝", "leo", "Client Signoff", "🌟"),
    ("One Line Quick Fix", "மூணு நாள் தேடின பக்கை ஒரே ஒரு ஸ்பேஸ் விட்டு சரி பண்ணிட்டேன்! 🎯💡", "leo", "Bug Slayer", "🎯"),
    ("Diwali Bonus Credited", "தீபாவளி போனஸ் அக்கவுண்ட்ல விழுந்தாச்சு.. பட்டாசு கிளப்புங்க! 🎆💸", "leo", "Bonus Day", "🎆"),
    ("Annamalai Power", "ஆண்டவன் சொல்றான் அருணாச்சலம் முடிக்கிறான்.. டாஸ்க் முடிஞ்சது! ⚡🦁", "leo", "Superstar Aura", "⚡"),
    ("Mankatha Game", "எங்க ஏரியா உள்ள வராதே.. 100% டெஸ்ட் கவரேஜ் அடிச்சு தூக்கியாச்சு! 🃏🔥", "leo", "Thala Swag", "🃏"),
    ("Soorarai Pottru Sky", "வானம் எல்லை இல்லடா.. நம்ம ஆப் ஆப் ஸ்டோர்ல நம்பர் ஒன் டிரெண்டிங்! ✈️🌟", "leo", "Suriya Spirit", "✈️"),
    ("Chepauk CSK Win", "தோனி கடைசி பந்துல சிக்ஸர் அடிச்ச மாதிரி கடைசி நிமிஷத்துல பக் பிக்ஸ்! 🏏🏆", "leo", "CSK Thala", "🏏"),
    ("Dindigul Biryani Treat", "திண்டுக்கல் தலப்பாகட்டி பிரியாணி சாப்பிட்டு பிராஜெக்ட் சக்சஸ் பார்ட்டி! 🍲🤤", "leo", "Biryani Feast", "🍲"),
    ("Fast Docker Deploy", "சர்வர் மைக்ரேஷன் ஒரு செகண்ட் கூட டவுன்டைம் இல்லாம முடிஞ்சுது! 🐳🚀", "leo", "DevOps Win", "🐳"),
    ("Senior Architect Praise", "சீனியர் ஆர்க்கிடெக்ட் என் கோட் டிசைன பாராட்டி மெயில் போட்டாரு! 💌✨", "leo", "Team Respect", "💌"),
    ("Weekend Relaxation", "அனைத்து வேலைகளும் முடிந்தது.. இனி ரெண்டு நாள் முழு ஓய்வு! 🧘‍♂️🏖️", "leo", "Pure Peace", "🧘‍♂️")
]

TAMIL_NEU = [
    ("Meeting Confusion Vadivelu", "எதுக்கு இந்த மீட்டிங் வெச்சீங்கன்னு யாருக்காவது தெரியுமா? 🤔😂", "fry", "Vadivelu Comedy", "🤷‍♂️"),
    ("OMR Toll Gate Traffic", "OMR டிராபிக்ல மாட்டிக்கிட்டு வாழ்க்கையோட அர்த்தத்த தேடுற தருணம் 🛵🚗", "fine", "Chennai IT Corridor", "🛵"),
    ("Spoken English Struggle", "இண்டர்வியூல இங்கிலீஷ் பேசும்போது நான் vs மனசுக்குள்ள நான் 🤐😂", "drake", "Interview Comedy", "🤐"),
    ("Tea Kadai Bench Discussion", "டீ கடையில உட்கார்ந்து உலக அரசியலையும் ஐடி கம்பெனியையும் அலசுற கூட்டம் ☕📰", "kermit", "Tea Kadai", "☕"),
    ("Standup Regular Dialogue", "நேத்து என்ன பண்ணீங்கன்னு கேட்டா யோசிக்க ரெண்டு நிமிஷம் வேணும் பாஸ் 📋⏳", "fine", "Daily Scrum", "📋"),
    ("Meals vs Variety Rice", "மதிய சாப்பாட்டுக்கு என்ன வாங்குறதுன்னு யோசிக்கவே ஒரு மணி நேரம் ஆகுது 🍱🤔", "fine", "Lunch Dilemma", "🍱"),
    ("Sleeping During Call", "ஆல்-ஹேண்ட்ஸ் மீட்டிங்ல மைக் ஆஃப் பண்ணிட்டு குறட்டை விடுற வாழ்க்கை 😴🛋️", "fine", "WFH Habit", "😴"),
    ("Beach to Tambaram Routine", "பீச் - தாம்பரம் ட்ரெயின்ல விண்டோ சீட் தேடுற எளிய மனிதனின் போராட்டம் 🚆🎧", "fine", "Local Train", "🚆"),
    ("Too Many JS Libraries", "பழையதை படிக்கிறதுக்குள்ள புதுசா பத்து லைப்ரரி வந்துடுது 💻🔄", "fine", "New Framework", "💻"),
    ("Chennai Sunny Afternoon", "சென்னையில மூணே சீசன் தான்: வெயில், அக்னி வெயில், அதையும் தாண்டிய வெயில் ☀️🔥", "fine", "Weather Drama", "☀️"),
    ("Gym Membership Postponed", "திங்கட்கிழமை ஜிம் போலாம்னு நினைச்சேன்.. ஆனா எந்த திங்கட்கிழமைன்னு சொல்லல 🏋️‍♂️🤷‍♂️", "cheems", "Gym Dream", "🏋️‍♂️"),
    ("Swiggy Cart Waiting", "கார்ட்ல போட்டு வெச்சிருக்கேன் ஆனா கூப்பன் கோடு வேலை செய்யல 🛒💭", "fine", "Online Cart", "🛒"),
    ("Who Wrote This Function", "இந்த கோட யார் எழுதினான்னு கிட் பிளேம் பாத்தா.. நானே தான் எழுதி இருக்கேன்! 🤦‍♂️🔍", "rollsafe", "Code History", "🤦‍♂️"),
    ("Saturday Afternoon Sleep", "சனிக்கிழமை மதியம் நல்லா தூங்கி எழுந்தா மணி ஆறு ஆயிடுது 🛌😴", "fine", "Weekend Routine", "🛌"),
    ("Camera Off Nodding", "கேமரா ஆஃப்ல இருக்கும்போது நாம என்ன பண்றோம்னு யாருக்கு தெரியும் 💻🙃", "fine", "Client Call", "💻"),
    ("Empty Documentation Tab", "டாக்குமெண்டேஷன் படிக்கலாம்னு தொறந்தா நாலு வரி தான் இருக்கு 📄👀", "fine", "Documentation", "📄"),
    ("Marina Beach Walking", "மெரினா பீச் காத்தை வாங்கிக்கிட்டே எதிர்காலத்தை யோசிக்கும் தருணம் 🏖️🚶‍♂️", "fine", "Beach Walk", "🏖️"),
    ("Auto Meter Bargaining", "சென்னை ஆட்டோக்காரரிடம் மீட்டர் போட சொல்லி அமைதியாக நிற்பது 🛺🤐", "fine", "Auto Drama", "🛺"),
    ("Filter Coffee Ritual", "மதிய உணவுக்குப் பின் சூடான பில்டர் காபி குடிக்கும் எளிய பழக்கம் ☕🫖", "fine", "Coffee Break", "☕"),
    ("Earphone Wire Tangle", "பாக்கெட்டிலிருந்து எடுத்த இயர்போன் சிக்கலை பத்து நிமிடம் எடுப்பது 🎧🪢", "fine", "Earphones Mess", "🎧"),
    ("Bus Pass Renewal Line", "மாதத்தின் முதல் நாள் பஸ் பாஸ் புதுப்பிக்க கியூவில் நிற்கும் நிலை 🚌🎫", "fine", "Bus Pass Queue", "🚌"),
    ("Online Course Tab Left", "வாங்கி வைத்த ஆன்லைன் கோர்ஸ் வீடியோவை முடிக்காமல் பார்க்கும் பார்வை 💻📚", "fine", "Course Pending", "💻"),
    ("Swiggy Order Tracking", "டெலிவரி பாய் மேப்பில் எங்கே வருகிறார் என்று தொடர்ந்து பார்ப்பது 🛵📍", "fine", "Food Tracking", "🛵"),
    ("Library Weekend Study", "அண்ணா நூற்றாண்டு நூலகத்தில் ஏசியில் அமர்ந்து வேடிக்கை பார்ப்பது 📚🏛️", "fine", "Library Time", "📚")
]

TAMIL_NEG = [
    ("Friday Prod Nightmare", "வெள்ளிக்கிழமை சாயங்காலம் புரொடக்ஷன்ல கோட் புஷ் பண்ணின என் நிலைமை 💀🚨", "bad", "Kollywood Sarcasm", "💀"),
    ("Aahaa Oru Mudivoda Thaan", "ஆஹா! ஒரு முடிவோடு தான் வந்துருக்காங்க.. கிளைன்ட் கிட்ட இருந்து தப்பிக்க முடியாது 🏃‍♂️💨", "sarcasticbear", "Vadivelu Panic", "🏃‍♂️"),
    ("Account Balance Zero", "சம்பளம் வந்த அடுத்த நிமிஷமே அக்கவுண்ட் ஜீரோ ஆயிடுச்சு.. கண்ணீர் மல்க বিদায় 💸😭", "bad", "Salary Vanished", "💸"),
    ("Vandhutanunga Da Call", "வந்துட்டானுங்கடா வந்துட்டானுங்க.. வீக்கெண்ட்ல வேலைய வச்சிக்கிட்டு வந்துட்டானுங்க 😭🚨", "bad", "Vadivelu Agony", "😭"),
    ("Production Server 502", "லைவ் சர்வர்ல 502 பேட் கேட்வே.. மேனேஜர் கண்ணுல அனல் பறக்குது! 🔥😱", "bad", "Crash Horror", "🔥"),
    ("Single Digit Percentage", "இவ்வளவு உழைச்சதுக்கு வெறும் 2% ஹைகா.. மனசு சுக்குநூறா உடைஞ்சு போச்சு 💔📉", "bad", "Appraisal Pain", "💔"),
    ("Leetcode Hard Nightmare", "ஈஸியான கம்பெனின்னு நெனச்சு போனா லீட்கோட் ஹார்ட் கேட்டு கதற விட்டுட்டாங்க 😭💻", "bad", "Interview Failure", "😭"),
    ("Sunday Night Panic Attack", "ஞாயிறு இரவு 9 மணிக்கு மேனேஜர் மெயில்.. தூக்கம் போச்சு! 📧😰", "bad", "Monday Fear", "📧"),
    ("Git Conflict Mess", "மெர்ஜ் பண்ணும்போது 40 ஃபைல் கான்பிளிக்ட்.. தலையில துண்ட போட்டுக்க வேண்டியது தான் 🤦‍♂️💀", "bad", "Merge Conflict", "🤦‍♂️"),
    ("2 AM Release Drama", "நடுராத்திரி ரெண்டு மணிக்கு ஆபிஸ்ல உக்காந்து அழுதுட்டு இருக்கேன் 🌙😭", "bad", "Overtime Hell", "😭"),
    ("Truncate Table Run On Prod", "டெஸ்ட்னு நினைச்சு புரொடக்ஷன் டேபிளை காலி பண்ணிட்டேன்.. அவ்ளோதான் வேலை காலி! 💥🛑", "bad", "Database Mistake", "💥"),
    ("EB Cut In Middle Of Code", "சார்ஜர் இல்லாம பேட்டரி 2% இருக்கும்போது கரண்ட் போயிடுச்சு.. பெருந்துயரம்! 🔌😱", "bad", "Power Cut", "🔌"),
    ("Micromanaging Lead", "நிமிஷத்துக்கு நிமிஷம் அப்டேட் கேக்குற மேனேஜர் கிட்ட இருந்து காப்பாத்துங்கடா 🤬😤", "bad", "Toxic Boss", "🤬"),
    ("Chennai House Rent Horror", "அட்வான்ஸ் பத்து மாசம், வாடகை பாதி சம்பளம்.. ரோட்டுல தான் படுக்கணும் 💸🏚️", "bad", "Rent Hike", "💸"),
    ("Goa Trip Cancelled Due To Work", "கோவா டிக்கெட் போட்டு வெச்சிருந்தேன்.. கடைசி நிமிஷத்துல ரிலீஸ்னு சொல்லி தடுத்துட்டாங்க 🏖️💔", "bad", "Cancelled Trip", "💔"),
    ("Spilled Coffee On MacBook", "லேப்டாப் மேல காபிய கொட்டிட்டேன்.. போர்டு போச்சு, ஃபைலும் போச்சு! ☕💻", "bad", "Laptop Dead", "💻"),
    ("Heavy Rain Stalled Bike", "சென்னையில் பெய்த திடீர் மழையில் பைக் தண்ணீரில் மூழ்கி நின்றுவிட்டது 🌧️🛵", "bad", "Rain Disaster", "🌧️"),
    ("Food Poisoning Biryani", "பழைய கடை பிரியாணி சாப்பிட்டு வாந்தி மயக்கம்.. ஆஸ்பத்திரியில் அட்மிட் 🤢🏥", "bad", "Food Sickness", "🤢"),
    ("Passport Damaged", "வெளிநாட்டு விசா நேர்காணலுக்கு முன் பாஸ்போர்ட்டில் காபி கொட்டியது 🛂😭", "bad", "Visa Agony", "🛂"),
    ("Production Memory Leak", "சர்வர் மெமரி லீக் ஆகி நள்ளிரவில் சைட்டே ஸ்தம்பித்தது 📉💥", "bad", "Out of Memory", "📉"),
    ("Stolen Laptop Bag", "ரயிலில் தூங்கும்போது லேப்டாப் பேக் திருடு போய்விட்டது.. பெருந்துயரம் 🎒😭", "bad", "Theft Nightmare", "😭"),
    ("Diwali Leave Rejected", "தீபாவளிக்கு சொந்த ஊருக்கு போக டிக்கெட் போட்டு லீவ் கேன்சல் பண்ணிட்டாங்க 🎆🚷", "bad", "Leave Denied", "🚷"),
    ("Critical Security Bug", "லைவ் ஆப்பில் பேமென்ட் கேட்வே உடைந்து ஹேக்கர்கள் பணம் எடுத்தனர் 🚨🔓", "bad", "Security Breach", "🚨"),
    ("Failed Final Round", "ஆறு ரவுண்ட் முடிந்து பைனல் ஹெச்ஆரில் நிராகரிப்பு.. தாங்க முடியாத வலி 🚪💔", "bad", "Final Reject", "💔")
]

# GLOBAL & HINGLISH (24 Pos, 24 Neu, 24 Neg)
GLOBAL_POS = [
    ("Leo DiCaprio Cheers", "When client says: 'Approved with zero revisions, payment released today' 😎🥂", "leo", "Absolute Cinema", "🥂"),
    ("Roll Safe Galaxy Brain", "You can't have bugs in production if you never release anything to production 🧠💡", "rollsafe", "Big Brain", "🧠"),
    ("Fixing Code by Deletion", "When you fix a 3-day production bug by deleting 200 lines of unused spaghetti code 🧹✨", "leo", "Pure Bliss", "✨"),
    ("Shipping Your Machine", "Developer: 'It works on my machine!' DevOps: 'Then we will ship your machine to the customer!' 💻📦", "cheems", "It Works On My Machine", "💻"),
    ("Coffee Running My Organs", "My blood is 10% water and 90% double espresso right now ☕⚡", "leo", "Coffee Energy", "☕"),
    ("Copy Pasted Script Worked", "The random 12-year-old answer on StackOverflow solved the entire company outage! 🏆🙌", "leo", "StackOverflow Hero", "🏆"),
    ("5 PM Friday Shutdown", "Closing all 87 browser tabs at 5 PM on Friday is pure spiritual therapy 🎉🏖️", "leo", "Friday Freedom", "🎉"),
    ("Clean Refactor Merge", "Reduced query latency from 14 seconds to 80 milliseconds.. feel like a wizard! 🧙‍♂️⚡", "leo", "Senior Architect", "🧙‍♂️"),
    ("Flawless Live Presentation", "Live demo worked on the first try in front of the VP of Engineering! 🌟👏", "leo", "Demo Success", "🌟"),
    ("Quarterly Bonus Released", "Company exceeded revenue targets and quarterly profit bonus just hit the bank! 💰🥳", "leo", "Bonus Announcement", "💰"),
    ("All Green Checkmarks", "Looking at 45 green checkmarks on GitHub Actions like a work of modern art 🟢✅", "leo", "CI Pipeline", "🟢"),
    ("Perfect Dark Theme", "Turning on OLED dark mode in IDE feels like giving my eyeballs a warm blanket 🌙🖤", "leo", "Dark Mode Bliss", "🌙"),
    ("Staff Engineer Letter", "Promotion finalized and compensation band raised to top tier! 🚀🥂", "leo", "Promotion Confirmed", "🚀"),
    ("Deep Focus Friday", "Zero meetings scheduled for the entire day.. pure uninterrupted coding paradise 🎧💻", "leo", "No Meetings Day", "🎧"),
    ("100 Percent Unit Test Pass", "All 800 automated test cases passed without a single flake! 🎯🔥", "leo", "Test Automation", "🎯"),
    ("Team Coffee Treat", "Manager bought everyone iced caramel macchiatos after sprint delivery! ☕🧁", "leo", "Coffee Treat", "☕"),
    ("Open Source Merge", "My pull request was merged into the official open-source Linux kernel repo! 🐧🌟", "leo", "Open Source Win", "🐧"),
    ("Zero Cloud Downtime", "Entire data center failed over with 99.999% uptime maintained! 🛡️⚡", "leo", "High Availability", "🛡️"),
    ("New Ergonomic Chair", "Company upgraded everyone to Herman Miller ergonomic chairs.. spine saved! 🪑✨", "leo", "Office Upgrade", "🪑"),
    ("Database Migration Win", "Migrated 50 terabytes of customer data with zero data loss! 💾🏆", "leo", "Database Master", "💾"),
    ("Hackathon Grand Prize", "Built a functional AI prototype in 24 hours and won first place! 🥇🚀", "leo", "Hackathon Champion", "🥇"),
    ("Smooth Performance Boost", "Eliminated memory leak and app startup time dropped by 80%! ⚡📱", "leo", "Mobile Win", "⚡"),
    ("First Job Offer", "Received my very first software engineer offer letter with great stock options! 📜🎉", "leo", "Career Milestone", "📜"),
    ("Holiday Bonus Party", "Year-end party with great food, drinks, and team celebration! 🍾🎊", "leo", "Year End Celebration", "🍾")
]

GLOBAL_NEU = [
    ("Doge Assembly vs CSS", "Developers in 1970 writing OS in assembly vs Me crying because CSS centering broke 🐶🐕", "cheems", "Developer History", "🐕"),
    ("6 Hours Automating", "Spending 6 hours writing a Python script to automate a task that takes 20 seconds manually 🤖🕒", "rollsafe", "Automation Trap", "🤖"),
    ("Global Tech Standstill", "If StackOverflow ever goes down for 24 hours, the world economy stops moving 🌍📉", "fine", "StackOverflow Down", "🌍"),
    ("80 Tabs Open", "Having 80 browser tabs open just so I don't forget something I will never read 🌐📑", "fine", "Browser Tabs", "🌐"),
    ("Yesterday Today Blockers", "Yesterday I investigated, today I will continue investigating, no blockers 📋⏳", "fine", "Agile Standup", "📋"),
    ("Mechanical Keyboard Click", "Click clack of mechanical switches making it sound like I am hacking the Pentagon ⌨️🎧", "fine", "Keyboard Sound", "⌨️"),
    ("Fix Typo Commit", "Commit history showing 'fixed bug', 'really fixed bug', 'final fix', 'final final fix' 📝🔍", "fine", "Git Commit Log", "📝"),
    ("Asking AI For Syntax", "Senior developer with 10 years experience asking AI how to write a regex 🤖💡", "rollsafe", "AI Assistants", "🤖"),
    ("Standing in Lunch Line", "Standing in cafeteria queue debating whether to get burrito or salad 🌯🥗", "fine", "Lunch Break", "🌯"),
    ("Restart For Update", "Clicking 'Remind me tomorrow' on OS system update for the 47th consecutive day 💻⏰", "fine", "Software Version", "💻"),
    ("TODO Add Comments", "Code comment says: // TODO: Clean this up later (Written 7 years ago) 📜⏳", "fine", "Documentation Reality", "📜"),
    ("Laptop Fan Airplane Mode", "Opening Docker and Android Studio causes laptop fan to sound like Boeing 747 takeoff 🛫💨", "fine", "Hardware Fan", "🛫"),
    ("Three Monitor Workspace", "Three 4K monitors: one for code, one for Slack, one for YouTube cat videos 🖥️🐱", "fine", "Desk Setup", "🖥️"),
    ("Two Hard Things In CS", "There are only two hard things in Computer Science: cache invalidation and naming things 🧠🏷️", "fine", "Naming Variables", "🧠"),
    ("Story Point Fibonacci", "Arguing whether converting button color is 2 story points or 3 Fibonacci points 🎲📊", "fine", "Sprint Velocity", "🎲"),
    ("Hydration Reminder App", "Installed 3 hydration tracking apps just to remember to drink one glass of water 💧📱", "fine", "Water Bottle", "💧"),
    ("Dark vs Light Theme", "Debating dark mode vs solarized light mode on developer forums for three hours 🌓💻", "fine", "Theme Debate", "🌓"),
    ("Waiting For Build", "Compiling C++ codebase gives me a legitimate 20-minute sword fighting break ⚔️☕", "fine", "Compiling Code", "⚔️"),
    ("Unused Python Virtualenv", "Having 15 virtual environments on laptop taking 40 GB of disk space 🐍📦", "fine", "Virtualenv Cleanup", "🐍"),
    ("Terminal Color Scheme", "Spending Friday afternoon customizing zsh terminal prompt with cool icons 💻🎨", "fine", "Zsh Rice", "💻"),
    ("Coffee Cup Collector", "Having four empty coffee mugs sitting on desk by 3 PM ☕🏺", "fine", "Desk Mugs", "☕"),
    ("Slack Status Emoji", "Changing Slack status emoji to 'Focusing' while browsing Reddit 🤫📱", "fine", "Slack Status", "🤫"),
    ("Re-reading Own Code", "Looking at code I wrote six months ago wondering what alien wrote it 👽📜", "fine", "Past Self", "👽"),
    ("Waiting For Test Suite", "Sitting quietly watching progress bar reach 99% and hanging for two minutes ⏳👀", "fine", "Test Wait", "⏳")
]

GLOBAL_NEG = [
    ("Disappointed Fan Sarcasm", "Waah! Kya service hai! 10 ghante line mein khada rakh ke bola server down hai 😭💀", "sarcasticbear", "Universal Sarcasm", "🤦‍♂️"),
    ("Spider-Man Multi-Team Blame", "Frontend dev, Backend dev, and DevOps pointing at each other during an outage 👈👉", "spiderman", "Blame Game", "🕷️"),
    ("Junior Git Force Push", "Senior dev watching intern type 'git push --force origin main' with cold sweat 😱🚨", "bad", "Senior Dev Panic", "😱"),
    ("Light Mode Blindness", "Opening an app that doesn't have dark mode at 2 AM feels like staring into the sun ☀️😵", "ch", "Dark Mode Only", "☀️"),
    ("500 Internal Error Nightmare", "Black Friday checkout page throwing 500 error.. millions disappearing every second 🚨📉", "bad", "Production Down", "🚨"),
    ("Browser Out Of Memory Crash", "Accidental infinite while loop froze entire browser and crashed un-saved work 💻💥", "bad", "Infinite Loop", "💥"),
    ("Mandatory Calendar Invite", "Received an unexpected invite titled 'Department Restructure Update' with HR copied 😰🚪", "bad", "Layoff Anxiety", "😰"),
    ("Lost Local Repository", "SSD corrupted and unsynced project work vanished into the void 😭💾", "bad", "Corrupt Hard Drive", "😭"),
    ("PagerDuty Pager Sirens", "PagerDuty alarm screaming at 3 AM on Sunday morning during thunderstorm 🚨📱", "bad", "Weekend On-Call", "🚨"),
    ("Log4j Style Emergency", "Critical zero-day security CVE dropped right before leaving for vacation 🛑🔓", "bad", "Zero Day Vulnerability", "🛑"),
    ("Activity Tracker Software", "Company installing mouse-movement tracker to monitor bathroom breaks 🖱️😡", "bad", "Micromanagement", "😡"),
    ("Sixth Consecutive 70hr Week", "Staring blankly at monitor feeling completely drained and burned out 💀🕯️", "bad", "Burnout Exhaustion", "💀"),
    ("MacBook Keyboard Ruined", "Spilled hot coffee straight into the cooling vents of my brand new work laptop ☕💻", "bad", "Spilled Coffee", "💻"),
    ("Surprise 10000 Dollar Bill", "Forgot to terminate GPU instance over weekend and got a $12,000 AWS bill 💸😱", "bad", "Cloud Bill Shock", "💸"),
    ("Zero Percent Merit Increase", "Told there is no budget for cost of living raises while CEO buys third yacht 💔📉", "bad", "Denied Raise", "💔"),
    ("Client Doubled Requirements", "Client added 40 new features two days before hard contractual deadline ⏳😫", "bad", "Scope Creep", "😫"),
    ("Production Database Drop", "Dropped the production users table during a live database migration at midnight 💣😱", "bad", "DB Catastrophe", "💣"),
    ("Expired SSL Certificate", "SSL certificate expired on main ecommerce domain during peak holiday sale 🔒🚫", "bad", "SSL Outage", "🔒"),
    ("Cancelled Paid Time Off", "Approved PTO cancelled by director due to an avoidable emergency sprint 🏖️🚫", "bad", "PTO Denied", "🚫"),
    ("Keyboard Water Spill", "Water spilled across mechanical keyboard causing keys to spam endlessly ⌨️💦", "bad", "Hardware Ruined", "⌨️"),
    ("Critical Ransomware Attack", "All internal servers encrypted by ransomware on Christmas Eve 🛑🔒", "bad", "Cyber Attack", "🛑"),
    ("Missed Interview Alarm", "Overslept through a final round FAANG interview due to phone dying overnight ⏰😭", "bad", "Interview Missed", "⏰"),
    ("Overheated GPU Melted", "GPU fans failed during overnight model training causing hardware permanent damage 🖥️🔥", "bad", "Hardware Melt", "🔥"),
    ("Unfair PIP Notice", "Put on performance improvement plan after reporting a critical safety bug 📄😡", "bad", "Toxic Workplace", "😡")
]

PALETTES = [
    ("#4f46e5", "#06b6d4"), ("#e11d48", "#f97316"), ("#0f766e", "#06b6d4"),
    ("#7c3aed", "#ec4899"), ("#334155", "#1e293b"), ("#b45309", "#78350f"),
    ("#065f46", "#10b981"), ("#1e1b4b", "#4338ca"), ("#991b1b", "#ef4444")
]

def seed_database():
    print(f"[*] Compiling master balanced dataset into {DB_PATH}...")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE memes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meme_id TEXT UNIQUE,
        title TEXT,
        language TEXT,
        tag TEXT,
        caption TEXT,
        image_url TEXT,
        fallback_bg_start TEXT,
        fallback_bg_end TEXT,
        emoji TEXT,
        sentiment TEXT,
        keywords TEXT
    )
    """)

    cursor.execute("CREATE INDEX idx_memes_lang ON memes(language);")
    cursor.execute("CREATE INDEX idx_memes_sentiment ON memes(sentiment);")

    all_groups = [
        ("Telugu", "positive", TELUGU_POS),
        ("Telugu", "neutral", TELUGU_NEU),
        ("Telugu", "negative", TELUGU_NEG),
        ("Bengali", "positive", BENGALI_POS),
        ("Bengali", "neutral", BENGALI_NEU),
        ("Bengali", "negative", BENGALI_NEG),
        ("Hindi", "positive", HINDI_POS),
        ("Hindi", "neutral", HINDI_NEU),
        ("Hindi", "negative", HINDI_NEG),
        ("Tamil", "positive", TAMIL_POS),
        ("Tamil", "neutral", TAMIL_NEU),
        ("Tamil", "negative", TAMIL_NEG),
        ("Global", "positive", GLOBAL_POS),
        ("Global", "neutral", GLOBAL_NEU),
        ("Global", "negative", GLOBAL_NEG),
    ]

    records = []
    idx = 0
    for lang, sent, items in all_groups:
        for title, caption, slug, tag, emoji in items:
            idx += 1
            pal = PALETTES[idx % len(PALETTES)]
            meme_id = f"{lang.lower()}-{idx}"
            image_url = f"https://api.memegen.link/images/{slug}/{title.replace(' ', '_')}/{lang}.png"
            keywords = f"{lang.lower()} {title.lower()} {tag.lower()} {sent}"
            records.append((
                meme_id, title, lang, tag, caption, image_url,
                pal[0], pal[1], emoji, sent, keywords
            ))

    cursor.executemany("""
    INSERT INTO memes (
        meme_id, title, language, tag, caption, image_url,
        fallback_bg_start, fallback_bg_end, emoji, sentiment, keywords
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)

    conn.commit()

    cursor.execute("SELECT COUNT(*), COUNT(DISTINCT caption) FROM memes")
    total, distinct = cursor.fetchone()

    cursor.execute("SELECT language, sentiment, COUNT(*) FROM memes GROUP BY language, sentiment")
    counts = cursor.fetchall()
    print(f"[SUCCESS] Seeded {total} unique memes ({distinct} distinct) into {DB_PATH}!")
    print(f"[*] Per-language/sentiment breakdown (15 groups x 24 items):")
    for l, s, c in counts:
        print(f"    {l:8s} | {s:8s} : {c}")
    conn.close()

if __name__ == "__main__":
    seed_database()
