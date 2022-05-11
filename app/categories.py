from enum import Enum

class FixedName(str, Enum):
    Rent = "家賃"
    Water = "水道代"
    Electric = "電気代"
    Gas = "ガス代"
    WiFi = "WiFi代"

class VariableName(str, Enum):
    Food = "食費"
    EatingOut = "外食費"
    Livingware = "生活用品"
    HomeAppliances = "生活家電"
    LivingFurniture = "生活家具"
    Income = "収入"

class CategoryName(str, Enum):
    FixedCostsCategories = "固定費カテゴリ"
    VariableCostsCategories = "変動費カテゴリ"

class Month(str, Enum):
    Jan = "Jan"
    Feb = "Feb"
    Mar = "MAr"
    Apr = "Apr"
    May = "May"
    Jun = "Jun"
    Jul = "Jul"
    Aug = "Aug"
    Sep = "Sep"
    Oct = "Oct"
    Nov = "Nov"
    Dec = "Dec"
