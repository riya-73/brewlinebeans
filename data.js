// =================== MENU ITEMS ===================
const img = q => `https://images.unsplash.com/${q}?auto=format&fit=crop&w=800&q=70`;

const menuItems = [
  { id:"m01", name:"Cappuccino", description:"Espresso topped with steamed milk and a thick layer of velvety foam.", price:220, category:"Hot Coffees", image:img("photo-1572442388796-11668a67e53d"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.018,unit:"kg"},{name:"Milk",quantity:0.18,unit:"L"},{name:"Sugar",quantity:0.01,unit:"kg"}]},
  { id:"m02", name:"Cafe Latte", description:"Smooth espresso layered with steamed milk and a light cap of foam.", price:240, category:"Hot Coffees", image:img("photo-1517256064527-09c73fc73e38"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.018,unit:"kg"},{name:"Milk",quantity:0.22,unit:"L"},{name:"Sugar",quantity:0.01,unit:"kg"}]},
  { id:"m03", name:"Flat White", description:"Double ristretto shots with silky micro-foamed whole milk.", price:250, category:"Hot Coffees", image:img("photo-1485808191679-5f86510681a2"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.022,unit:"kg"},{name:"Milk",quantity:0.16,unit:"L"}]},
  { id:"m04", name:"Americano", description:"Rich espresso shots topped with hot water for a clean, bold cup.", price:180, category:"Hot Coffees", image:img("photo-1497935586351-b67a49e012bf"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.02,unit:"kg"},{name:"Sugar",quantity:0.008,unit:"kg"}]},
  { id:"m05", name:"Mocha", description:"Espresso meets steamed milk and rich chocolate syrup, finished with cream.", price:270, category:"Hot Coffees", image:img("photo-1578314675229-bcd2eea8c80a"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.018,unit:"kg"},{name:"Milk",quantity:0.2,unit:"L"},{name:"Chocolate Syrup",quantity:0.03,unit:"L"},{name:"Whipped Cream",quantity:0.02,unit:"kg"}]},
  { id:"m06", name:"Caramel Latte", description:"Velvety latte swirled with house-made caramel and a buttery drizzle.", price:280, category:"Hot Coffees", image:img("photo-1461023058943-07fcbe16d735"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.018,unit:"kg"},{name:"Milk",quantity:0.22,unit:"L"},{name:"Caramel Syrup",quantity:0.025,unit:"L"}]},
  { id:"m07", name:"Hazelnut Latte", description:"Roasted hazelnut syrup folded into a creamy latte for nutty warmth.", price:285, category:"Hot Coffees", image:img("photo-1542990253-0d0f5be5f0ed"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.018,unit:"kg"},{name:"Milk",quantity:0.22,unit:"L"},{name:"Hazelnut Syrup",quantity:0.025,unit:"L"}]},
  { id:"m08", name:"Vanilla Latte", description:"Smooth latte sweetened with house vanilla syrup.", price:270, category:"Hot Coffees", image:img("photo-1551030173-122aabc4489c"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.018,unit:"kg"},{name:"Milk",quantity:0.22,unit:"L"},{name:"Vanilla Syrup",quantity:0.025,unit:"L"}]},
  { id:"m09", name:"Espresso", description:"A pure double shot of our signature dark roast espresso.", price:150, category:"Hot Coffees", image:img("photo-1510707577719-ae7c14805e3a"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.018,unit:"kg"}]},
  { id:"m10", name:"Macchiato", description:"Espresso marked with a dollop of foamed milk for a bold finish.", price:210, category:"Hot Coffees", image:img("photo-1534687941688-651ccaafbff8"), available:false, ingredients:[{name:"Coffee Beans",quantity:0.018,unit:"kg"},{name:"Milk",quantity:0.05,unit:"L"}]},
  { id:"m11", name:"Iced Latte", description:"Chilled espresso poured over ice with cold milk for a refreshing pick-me-up.", price:260, category:"Cold Coffees", image:img("photo-1517701604599-bb29b565090c"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.018,unit:"kg"},{name:"Milk",quantity:0.2,unit:"L"},{name:"Ice Cubes",quantity:0.12,unit:"kg"}]},
  { id:"m12", name:"Cold Brew", description:"Slow-steeped 18-hour cold brew over ice — smooth, less acidic.", price:280, category:"Cold Coffees", image:img("photo-1461023058943-07fcbe16d735"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.025,unit:"kg"},{name:"Ice Cubes",quantity:0.15,unit:"kg"}]},
  { id:"m13", name:"Iced Americano", description:"Bold espresso topped with chilled water and ice.", price:200, category:"Cold Coffees", image:img("photo-1542181961-9590d0c79dab"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.02,unit:"kg"},{name:"Ice Cubes",quantity:0.12,unit:"kg"}]},
  { id:"m14", name:"Iced Mocha", description:"Espresso, chocolate and cold milk over ice with a swirl of cream.", price:290, category:"Cold Coffees", image:img("photo-1572490122747-3968b75cc699"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.018,unit:"kg"},{name:"Milk",quantity:0.18,unit:"L"},{name:"Chocolate Syrup",quantity:0.03,unit:"L"},{name:"Ice Cubes",quantity:0.12,unit:"kg"},{name:"Whipped Cream",quantity:0.02,unit:"kg"}]},
  { id:"m15", name:"Iced Caramel Macchiato", description:"Vanilla, milk and espresso layered over ice, finished with caramel.", price:295, category:"Cold Coffees", image:img("photo-1568901346375-23c9450c58cd"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.018,unit:"kg"},{name:"Milk",quantity:0.2,unit:"L"},{name:"Caramel Syrup",quantity:0.025,unit:"L"},{name:"Vanilla Syrup",quantity:0.015,unit:"L"},{name:"Ice Cubes",quantity:0.12,unit:"kg"}]},
  { id:"m16", name:"Nitro Cold Brew", description:"Cold brew infused with nitrogen for a creamy, cascading pour.", price:310, category:"Cold Coffees", image:img("photo-1559496417-e7f25cb247f3"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.025,unit:"kg"},{name:"Ice Cubes",quantity:0.1,unit:"kg"}]},
  { id:"m17", name:"English Breakfast Tea", description:"Robust black tea blend, perfect with a splash of warm milk.", price:150, category:"Teas", image:img("photo-1597481499750-3e6b22637e12"), available:true, ingredients:[{name:"Tea Leaves",quantity:0.005,unit:"kg"},{name:"Milk",quantity:0.05,unit:"L"},{name:"Sugar",quantity:0.008,unit:"kg"}]},
  { id:"m18", name:"Masala Chai", description:"Spiced black tea simmered with milk, cardamom and ginger.", price:140, category:"Teas", image:img("photo-1571934811356-5cc061b6821f"), available:true, ingredients:[{name:"Tea Leaves",quantity:0.006,unit:"kg"},{name:"Milk",quantity:0.15,unit:"L"},{name:"Sugar",quantity:0.012,unit:"kg"},{name:"Cinnamon Powder",quantity:0.002,unit:"kg"}]},
  { id:"m19", name:"Green Tea", description:"Delicate sencha leaves with grassy, refreshing notes.", price:140, category:"Teas", image:img("photo-1556679343-c7306c1976bc"), available:true, ingredients:[{name:"Tea Leaves",quantity:0.004,unit:"kg"}]},
  { id:"m20", name:"Iced Peach Tea", description:"Chilled black tea infused with sweet peach and lemon.", price:170, category:"Teas", image:img("photo-1556679343-c7306c1976bc"), available:true, ingredients:[{name:"Tea Leaves",quantity:0.005,unit:"kg"},{name:"Sugar",quantity:0.015,unit:"kg"},{name:"Ice Cubes",quantity:0.12,unit:"kg"}]},
  { id:"m21", name:"Vanilla Frappe", description:"Blended vanilla, milk and ice topped with whipped cream.", price:300, category:"Frappes", image:img("photo-1572286258217-215cf8e9d99d"), available:true, ingredients:[{name:"Milk",quantity:0.2,unit:"L"},{name:"Vanilla Syrup",quantity:0.03,unit:"L"},{name:"Ice Cubes",quantity:0.18,unit:"kg"},{name:"Whipped Cream",quantity:0.025,unit:"kg"},{name:"Sugar",quantity:0.012,unit:"kg"}]},
  { id:"m22", name:"Chocolate Frappe", description:"Rich cocoa and milk blended with ice, crowned with whipped cream.", price:310, category:"Frappes", image:img("photo-1572490122747-3968b75cc699"), available:true, ingredients:[{name:"Milk",quantity:0.2,unit:"L"},{name:"Chocolate Syrup",quantity:0.04,unit:"L"},{name:"Cocoa Powder",quantity:0.008,unit:"kg"},{name:"Ice Cubes",quantity:0.18,unit:"kg"},{name:"Whipped Cream",quantity:0.025,unit:"kg"}]},
  { id:"m23", name:"Caramel Frappe", description:"Buttery caramel blended with espresso, milk and ice.", price:320, category:"Frappes", image:img("photo-1461023058943-07fcbe16d735"), available:true, ingredients:[{name:"Coffee Beans",quantity:0.015,unit:"kg"},{name:"Milk",quantity:0.2,unit:"L"},{name:"Caramel Syrup",quantity:0.035,unit:"L"},{name:"Ice Cubes",quantity:0.18,unit:"kg"},{name:"Whipped Cream",quantity:0.025,unit:"kg"}]},
  { id:"m24", name:"Mocha Frappe", description:"Coffee, chocolate and milk blended to icy perfection.", price:320, category:"Frappes", image:img("photo-1572442388796-11668a67e53d"), available:false, ingredients:[{name:"Coffee Beans",quantity:0.015,unit:"kg"},{name:"Milk",quantity:0.2,unit:"L"},{name:"Chocolate Syrup",quantity:0.035,unit:"L"},{name:"Ice Cubes",quantity:0.18,unit:"kg"},{name:"Whipped Cream",quantity:0.025,unit:"kg"}]},
  { id:"m25", name:"Hazelnut Frappe", description:"Toasted hazelnut blended cold with milk and ice.", price:315, category:"Frappes", image:img("photo-1542990253-0d0f5be5f0ed"), available:true, ingredients:[{name:"Milk",quantity:0.2,unit:"L"},{name:"Hazelnut Syrup",quantity:0.035,unit:"L"},{name:"Ice Cubes",quantity:0.18,unit:"kg"},{name:"Whipped Cream",quantity:0.025,unit:"kg"}]},
  { id:"m26", name:"Blueberry Muffin", description:"Soft buttermilk muffin bursting with wild blueberries.", price:160, category:"Pastries", image:img("photo-1607958996333-41aef7caefaa"), available:true, ingredients:[{name:"Muffins",quantity:1,unit:"pcs"}]},
  { id:"m27", name:"Butter Croissant", description:"Flaky French-style croissant with layers of butter.", price:180, category:"Pastries", image:img("photo-1555507036-ab1f4038808a"), available:true, ingredients:[{name:"Croissants",quantity:1,unit:"pcs"}]},
  { id:"m28", name:"Chocolate Croissant", description:"Buttery croissant filled with dark chocolate batons.", price:210, category:"Pastries", image:img("photo-1623334044303-241021148842"), available:true, ingredients:[{name:"Croissants",quantity:1,unit:"pcs"},{name:"Chocolate Syrup",quantity:0.02,unit:"L"}]},
  { id:"m29", name:"Cinnamon Roll", description:"Warm swirl pastry brushed with cinnamon sugar glaze.", price:200, category:"Pastries", image:img("photo-1509365465985-25d11c17e812"), available:true, ingredients:[{name:"Muffins",quantity:1,unit:"pcs"},{name:"Cinnamon Powder",quantity:0.003,unit:"kg"},{name:"Sugar",quantity:0.015,unit:"kg"}]},
  { id:"m30", name:"Chicken Club Sandwich", description:"Grilled chicken, lettuce, tomato and cheese on toasted bread.", price:290, category:"Sandwiches", image:img("photo-1528735602780-2552fd46c7af"), available:true, ingredients:[{name:"Sandwich Bread",quantity:2,unit:"pcs"},{name:"Chicken Filling",quantity:0.08,unit:"kg"},{name:"Lettuce",quantity:0.02,unit:"kg"},{name:"Tomatoes",quantity:0.03,unit:"kg"},{name:"Cheese",quantity:0.025,unit:"kg"}]},
  { id:"m31", name:"Cheese & Tomato Panini", description:"Toasted panini with melted cheese, ripe tomatoes and basil.", price:260, category:"Sandwiches", image:img("photo-1592415499556-74fcb9f18667"), available:true, ingredients:[{name:"Sandwich Bread",quantity:2,unit:"pcs"},{name:"Cheese",quantity:0.04,unit:"kg"},{name:"Tomatoes",quantity:0.035,unit:"kg"}]},
  { id:"m32", name:"Veggie Delight Sandwich", description:"Garden vegetables, cheese and herb spread on multigrain bread.", price:240, category:"Sandwiches", image:img("photo-1539252554935-80c8cabf1bf6"), available:true, ingredients:[{name:"Sandwich Bread",quantity:2,unit:"pcs"},{name:"Lettuce",quantity:0.025,unit:"kg"},{name:"Tomatoes",quantity:0.03,unit:"kg"},{name:"Cheese",quantity:0.02,unit:"kg"}]},
];

// =================== INVENTORY ===================
const inventory = [
  {id:"ing-01",name:"Coffee Beans",currentStock:48,reorderLevel:25,unit:"kg"},
  {id:"ing-02",name:"Milk",currentStock:120,reorderLevel:80,unit:"L"},
  {id:"ing-03",name:"Sugar",currentStock:22,reorderLevel:15,unit:"kg"},
  {id:"ing-04",name:"Tea Leaves",currentStock:9,reorderLevel:10,unit:"kg"},
  {id:"ing-05",name:"Chocolate Syrup",currentStock:14,reorderLevel:12,unit:"L"},
  {id:"ing-06",name:"Caramel Syrup",currentStock:6,reorderLevel:10,unit:"L"},
  {id:"ing-07",name:"Vanilla Syrup",currentStock:11,reorderLevel:8,unit:"L"},
  {id:"ing-08",name:"Whipped Cream",currentStock:7,reorderLevel:6,unit:"kg"},
  {id:"ing-09",name:"Ice Cubes",currentStock:95,reorderLevel:50,unit:"kg"},
  {id:"ing-10",name:"Cocoa Powder",currentStock:3,reorderLevel:5,unit:"kg"},
  {id:"ing-11",name:"Cinnamon Powder",currentStock:2.4,reorderLevel:2,unit:"kg"},
  {id:"ing-12",name:"Hazelnut Syrup",currentStock:5,reorderLevel:6,unit:"L"},
  {id:"ing-13",name:"Oat Milk",currentStock:28,reorderLevel:20,unit:"L"},
  {id:"ing-14",name:"Almond Milk",currentStock:18,reorderLevel:20,unit:"L"},
  {id:"ing-15",name:"Croissants",currentStock:42,reorderLevel:30,unit:"pcs"},
  {id:"ing-16",name:"Muffins",currentStock:18,reorderLevel:25,unit:"pcs"},
  {id:"ing-17",name:"Sandwich Bread",currentStock:60,reorderLevel:40,unit:"pcs"},
  {id:"ing-18",name:"Cheese",currentStock:8.5,reorderLevel:6,unit:"kg"},
  {id:"ing-19",name:"Chicken Filling",currentStock:4,reorderLevel:5,unit:"kg"},
  {id:"ing-20",name:"Lettuce",currentStock:3.2,reorderLevel:3,unit:"kg"},
  {id:"ing-21",name:"Tomatoes",currentStock:6.8,reorderLevel:5,unit:"kg"},
  {id:"ing-22",name:"Paper Cups",currentStock:850,reorderLevel:500,unit:"pcs"},
  {id:"ing-23",name:"Cup Lids",currentStock:420,reorderLevel:500,unit:"pcs"},
  {id:"ing-24",name:"Napkins",currentStock:1500,reorderLevel:800,unit:"pcs"},
  {id:"ing-25",name:"Stirrers",currentStock:260,reorderLevel:400,unit:"pcs"},
];

function statusFor(item) {
  const ratio = item.currentStock / item.reorderLevel;
  if (item.currentStock < item.reorderLevel * 0.6) return "Critical";
  if (ratio < 1) return "Low Stock";
  return "Healthy";
}

// =================== SUPPLIERS ===================
const suppliers = [
  {id:"s01",name:"BrewCorp",ingredient:"Coffee Beans",pricePerUnit:500,unit:"kg",leadTimeDays:2,qualityScore:9.5,reliability:98},
  {id:"s02",name:"BeanMasters",ingredient:"Coffee Beans",pricePerUnit:450,unit:"kg",leadTimeDays:4,qualityScore:8.2,reliability:90},
  {id:"s03",name:"Highland Roasters",ingredient:"Coffee Beans",pricePerUnit:520,unit:"kg",leadTimeDays:3,qualityScore:9.7,reliability:96},
  {id:"s04",name:"DairyFresh",ingredient:"Milk",pricePerUnit:60,unit:"L",leadTimeDays:1,qualityScore:9.8,reliability:99},
  {id:"s05",name:"PureMoo Dairy",ingredient:"Milk",pricePerUnit:55,unit:"L",leadTimeDays:1,qualityScore:9.2,reliability:95},
  {id:"s06",name:"GreenPastures",ingredient:"Milk",pricePerUnit:58,unit:"L",leadTimeDays:2,qualityScore:9.4,reliability:94},
  {id:"s07",name:"SweetCo",ingredient:"Sugar",pricePerUnit:45,unit:"kg",leadTimeDays:3,qualityScore:8.8,reliability:92},
  {id:"s08",name:"CaneKings",ingredient:"Sugar",pricePerUnit:42,unit:"kg",leadTimeDays:5,qualityScore:8.3,reliability:88},
  {id:"s09",name:"Assam Tea Co.",ingredient:"Tea Leaves",pricePerUnit:380,unit:"kg",leadTimeDays:4,qualityScore:9.6,reliability:97},
  {id:"s10",name:"Darjeeling Garden",ingredient:"Tea Leaves",pricePerUnit:420,unit:"kg",leadTimeDays:5,qualityScore:9.9,reliability:96},
  {id:"s11",name:"SyrupHouse",ingredient:"Chocolate Syrup",pricePerUnit:320,unit:"L",leadTimeDays:3,qualityScore:9.0,reliability:93},
  {id:"s12",name:"CocoaCraft",ingredient:"Chocolate Syrup",pricePerUnit:295,unit:"L",leadTimeDays:4,qualityScore:8.5,reliability:90},
  {id:"s13",name:"SyrupHouse",ingredient:"Caramel Syrup",pricePerUnit:340,unit:"L",leadTimeDays:3,qualityScore:9.1,reliability:93},
  {id:"s14",name:"Golden Drizzle",ingredient:"Caramel Syrup",pricePerUnit:310,unit:"L",leadTimeDays:5,qualityScore:8.6,reliability:89},
  {id:"s15",name:"SyrupHouse",ingredient:"Vanilla Syrup",pricePerUnit:360,unit:"L",leadTimeDays:3,qualityScore:9.2,reliability:94},
  {id:"s16",name:"Madagascar Flavors",ingredient:"Vanilla Syrup",pricePerUnit:410,unit:"L",leadTimeDays:6,qualityScore:9.8,reliability:95},
  {id:"s17",name:"CreamWorks",ingredient:"Whipped Cream",pricePerUnit:220,unit:"kg",leadTimeDays:2,qualityScore:9.3,reliability:96},
  {id:"s18",name:"DairyFresh",ingredient:"Whipped Cream",pricePerUnit:240,unit:"kg",leadTimeDays:1,qualityScore:9.5,reliability:98},
  {id:"s19",name:"FrostLogistics",ingredient:"Ice Cubes",pricePerUnit:15,unit:"kg",leadTimeDays:1,qualityScore:9.0,reliability:97},
  {id:"s20",name:"ChillSupply",ingredient:"Ice Cubes",pricePerUnit:12,unit:"kg",leadTimeDays:2,qualityScore:8.5,reliability:92},
  {id:"s21",name:"CocoaCraft",ingredient:"Cocoa Powder",pricePerUnit:480,unit:"kg",leadTimeDays:4,qualityScore:9.4,reliability:95},
  {id:"s22",name:"SpiceRoute",ingredient:"Cinnamon Powder",pricePerUnit:650,unit:"kg",leadTimeDays:3,qualityScore:9.5,reliability:94},
  {id:"s23",name:"Kerala Spices",ingredient:"Cinnamon Powder",pricePerUnit:600,unit:"kg",leadTimeDays:5,qualityScore:9.0,reliability:90},
  {id:"s24",name:"SyrupHouse",ingredient:"Hazelnut Syrup",pricePerUnit:390,unit:"L",leadTimeDays:3,qualityScore:9.0,reliability:92},
  {id:"s25",name:"NuttyCraft",ingredient:"Hazelnut Syrup",pricePerUnit:360,unit:"L",leadTimeDays:5,qualityScore:8.7,reliability:89},
  {id:"s26",name:"PlantPure",ingredient:"Oat Milk",pricePerUnit:140,unit:"L",leadTimeDays:2,qualityScore:9.3,reliability:95},
  {id:"s27",name:"OatHarvest",ingredient:"Oat Milk",pricePerUnit:130,unit:"L",leadTimeDays:3,qualityScore:8.9,reliability:91},
  {id:"s28",name:"PlantPure",ingredient:"Almond Milk",pricePerUnit:160,unit:"L",leadTimeDays:2,qualityScore:9.2,reliability:94},
  {id:"s29",name:"NutriNuts",ingredient:"Almond Milk",pricePerUnit:150,unit:"L",leadTimeDays:3,qualityScore:8.8,reliability:90},
  {id:"s30",name:"BakeHouse",ingredient:"Croissants",pricePerUnit:35,unit:"pcs",leadTimeDays:1,qualityScore:9.4,reliability:97},
  {id:"s31",name:"ParisOven",ingredient:"Croissants",pricePerUnit:40,unit:"pcs",leadTimeDays:1,qualityScore:9.7,reliability:96},
  {id:"s32",name:"BakeHouse",ingredient:"Muffins",pricePerUnit:30,unit:"pcs",leadTimeDays:1,qualityScore:9.2,reliability:96},
  {id:"s33",name:"SweetCrumb",ingredient:"Muffins",pricePerUnit:28,unit:"pcs",leadTimeDays:2,qualityScore:8.8,reliability:92},
  {id:"s34",name:"BakeHouse",ingredient:"Sandwich Bread",pricePerUnit:8,unit:"pcs",leadTimeDays:1,qualityScore:9.0,reliability:96},
  {id:"s35",name:"WheatMill",ingredient:"Sandwich Bread",pricePerUnit:7,unit:"pcs",leadTimeDays:2,qualityScore:8.6,reliability:91},
  {id:"s36",name:"DairyFresh",ingredient:"Cheese",pricePerUnit:520,unit:"kg",leadTimeDays:2,qualityScore:9.6,reliability:98},
  {id:"s37",name:"CheeseValley",ingredient:"Cheese",pricePerUnit:480,unit:"kg",leadTimeDays:3,qualityScore:9.2,reliability:93},
  {id:"s38",name:"FarmPoultry",ingredient:"Chicken Filling",pricePerUnit:280,unit:"kg",leadTimeDays:2,qualityScore:9.3,reliability:95},
  {id:"s39",name:"PrimeMeats",ingredient:"Chicken Filling",pricePerUnit:310,unit:"kg",leadTimeDays:1,qualityScore:9.6,reliability:97},
  {id:"s40",name:"FreshFarms",ingredient:"Lettuce",pricePerUnit:90,unit:"kg",leadTimeDays:1,qualityScore:9.1,reliability:95},
  {id:"s41",name:"GreenLeaf",ingredient:"Lettuce",pricePerUnit:85,unit:"kg",leadTimeDays:2,qualityScore:8.8,reliability:92},
  {id:"s42",name:"FreshFarms",ingredient:"Tomatoes",pricePerUnit:70,unit:"kg",leadTimeDays:1,qualityScore:9.0,reliability:95},
  {id:"s43",name:"RedHarvest",ingredient:"Tomatoes",pricePerUnit:65,unit:"kg",leadTimeDays:2,qualityScore:8.7,reliability:91},
  {id:"s44",name:"PaperPak",ingredient:"Paper Cups",pricePerUnit:4.5,unit:"pcs",leadTimeDays:5,qualityScore:9.0,reliability:94},
  {id:"s45",name:"EcoServe",ingredient:"Paper Cups",pricePerUnit:5.2,unit:"pcs",leadTimeDays:4,qualityScore:9.4,reliability:96},
  {id:"s46",name:"PaperPak",ingredient:"Cup Lids",pricePerUnit:2.5,unit:"pcs",leadTimeDays:5,qualityScore:8.9,reliability:93},
  {id:"s47",name:"PaperPak",ingredient:"Napkins",pricePerUnit:0.6,unit:"pcs",leadTimeDays:5,qualityScore:8.8,reliability:94},
  {id:"s48",name:"EcoServe",ingredient:"Stirrers",pricePerUnit:0.4,unit:"pcs",leadTimeDays:4,qualityScore:9.0,reliability:95},
];

// =================== PURCHASES ===================
function makePurchases() {
  const seed = [
    ["Coffee Beans","BrewCorp",500,"kg",[10,12,8,15,20,9,11]],
    ["Coffee Beans","BeanMasters",450,"kg",[10,14,9]],
    ["Milk","DairyFresh",60,"L",[80,100,90,120,75,95,110,85]],
    ["Milk","PureMoo Dairy",55,"L",[60,70,50]],
    ["Sugar","SweetCo",45,"kg",[25,20,30,22]],
    ["Tea Leaves","Assam Tea Co.",380,"kg",[8,6,10]],
    ["Tea Leaves","Darjeeling Garden",420,"kg",[4,5]],
    ["Chocolate Syrup","SyrupHouse",320,"L",[12,10,15]],
    ["Caramel Syrup","Golden Drizzle",310,"L",[8,10]],
    ["Vanilla Syrup","Madagascar Flavors",410,"L",[6,8]],
    ["Whipped Cream","CreamWorks",220,"kg",[5,7,6]],
    ["Ice Cubes","FrostLogistics",15,"kg",[80,100,120,90]],
    ["Cocoa Powder","CocoaCraft",480,"kg",[3,4]],
    ["Cinnamon Powder","SpiceRoute",650,"kg",[2,1.5]],
    ["Hazelnut Syrup","NuttyCraft",360,"L",[5,6]],
    ["Oat Milk","PlantPure",140,"L",[20,25]],
    ["Almond Milk","NutriNuts",150,"L",[18,22]],
    ["Croissants","ParisOven",40,"pcs",[60,80,70]],
    ["Muffins","BakeHouse",30,"pcs",[50,40,60]],
    ["Sandwich Bread","WheatMill",7,"pcs",[80,100]],
    ["Cheese","DairyFresh",520,"kg",[6,8]],
    ["Chicken Filling","FarmPoultry",280,"kg",[5,4]],
    ["Lettuce","FreshFarms",90,"kg",[3,4]],
    ["Tomatoes","RedHarvest",65,"kg",[5,6]],
    ["Paper Cups","PaperPak",4.5,"pcs",[1000,1500]],
  ];
  const result = [];
  let counter = 1000;
  const today = new Date("2025-06-08");
  let dayOffset = 0;
  for (const [ingredient, supplier, price, unit, qtys] of seed) {
    for (const q of qtys) {
      const d = new Date(today);
      d.setDate(d.getDate() - dayOffset);
      result.push({
        id: `PO-${counter++}`,
        date: d.toISOString().slice(0, 10),
        ingredient, supplier, quantity: q, unit,
        totalCost: Math.round(q * price),
      });
      dayOffset += 2;
    }
  }
  return result.sort((a, b) => a.date < b.date ? 1 : -1);
}
const purchases = makePurchases();
