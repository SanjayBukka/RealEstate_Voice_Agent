"""Sample property data for the Real Estate AI Agent"""

PROPERTIES = [
    # Dallas Properties
    {
        "id": "DAL001",
        "type": "plot",
        "location": "Dallas",
        "area": "North Dallas",
        "price": 350000,
        "size": "0.5 acres",
        "features": ["Corner lot", "Near schools", "Utilities ready"],
        "available": True
    },
    {
        "id": "DAL002",
        "type": "plot",
        "location": "Dallas",
        "area": "Frisco",
        "price": 420000,
        "size": "0.75 acres",
        "features": ["Lake view", "Gated community", "HOA included"],
        "available": True
    },
    {
        "id": "DAL003",
        "type": "house",
        "location": "Dallas",
        "area": "Plano",
        "price": 550000,
        "size": "2,400 sq ft",
        "bedrooms": 4,
        "bathrooms": 3,
        "features": ["Modern kitchen", "Pool ready", "2 car garage"],
        "available": True
    },
    {
        "id": "DAL004",
        "type": "apartment",
        "location": "Dallas",
        "area": "Downtown Dallas",
        "price": 280000,
        "size": "1,200 sq ft",
        "bedrooms": 2,
        "bathrooms": 2,
        "features": ["City view", "Gym access", "Concierge"],
        "available": True
    },
    
    # Austin Properties
    {
        "id": "AUS001",
        "type": "plot",
        "location": "Austin",
        "area": "Round Rock",
        "price": 380000,
        "size": "0.6 acres",
        "features": ["Hill country views", "Near tech corridor"],
        "available": True
    },
    {
        "id": "AUS002",
        "type": "house",
        "location": "Austin",
        "area": "Cedar Park",
        "price": 620000,
        "size": "2,800 sq ft",
        "bedrooms": 4,
        "bathrooms": 3,
        "features": ["Smart home", "Solar panels", "Large backyard"],
        "available": True
    },
    {
        "id": "AUS003",
        "type": "villa",
        "location": "Austin",
        "area": "Lake Travis",
        "price": 950000,
        "size": "3,500 sq ft",
        "bedrooms": 5,
        "bathrooms": 4,
        "features": ["Lake access", "Private dock", "Wine cellar"],
        "available": True
    },
    
    # Houston Properties
    {
        "id": "HOU001",
        "type": "plot",
        "location": "Houston",
        "area": "The Woodlands",
        "price": 320000,
        "size": "0.4 acres",
        "features": ["Wooded lot", "Top-rated schools", "Walking trails"],
        "available": True
    },
    {
        "id": "HOU002",
        "type": "house",
        "location": "Houston",
        "area": "Katy",
        "price": 480000,
        "size": "2,200 sq ft",
        "bedrooms": 3,
        "bathrooms": 2,
        "features": ["New construction", "Energy efficient", "Community pool"],
        "available": True
    },
    {
        "id": "HOU003",
        "type": "apartment",
        "location": "Houston",
        "area": "Galleria",
        "price": 350000,
        "size": "1,500 sq ft",
        "bedrooms": 2,
        "bathrooms": 2,
        "features": ["High rise", "Rooftop pool", "24/7 security"],
        "available": True
    },
    
    # San Antonio Properties
    {
        "id": "SAT001",
        "type": "plot",
        "location": "San Antonio",
        "area": "Stone Oak",
        "price": 280000,
        "size": "0.5 acres",
        "features": ["Hilltop lot", "Great views", "Near shopping"],
        "available": True
    },
    {
        "id": "SAT002",
        "type": "house",
        "location": "San Antonio",
        "area": "Alamo Heights",
        "price": 520000,
        "size": "2,600 sq ft",
        "bedrooms": 4,
        "bathrooms": 3,
        "features": ["Historic charm", "Updated interior", "Large oaks"],
        "available": True
    },
    
    # Phoenix Properties
    {
        "id": "PHX001",
        "type": "plot",
        "location": "Phoenix",
        "area": "Scottsdale",
        "price": 450000,
        "size": "0.8 acres",
        "features": ["Desert landscaping", "Mountain views", "Golf nearby"],
        "available": True
    },
    {
        "id": "PHX002",
        "type": "villa",
        "location": "Phoenix",
        "area": "Paradise Valley",
        "price": 1200000,
        "size": "4,200 sq ft",
        "bedrooms": 5,
        "bathrooms": 5,
        "features": ["Resort-style pool", "Guest house", "Gourmet kitchen"],
        "available": True
    }
]

def get_properties_summary():
    """Get a formatted summary of all properties for the LLM context"""
    summary = []
    for prop in PROPERTIES:
        if prop["available"]:
            prop_info = f"- {prop['type'].title()} in {prop['area']}, {prop['location']}: ${prop['price']:,}"
            if "bedrooms" in prop:
                prop_info += f" | {prop['bedrooms']}BR/{prop['bathrooms']}BA"
            prop_info += f" | {prop['size']}"
            prop_info += f" | Features: {', '.join(prop['features'][:2])}"
            summary.append(prop_info)
    return "\n".join(summary)

def filter_properties(location=None, max_budget=None, property_type=None):
    """Filter properties based on criteria"""
    filtered = []
    for prop in PROPERTIES:
        if not prop["available"]:
            continue
        if location and location.lower() not in prop["location"].lower():
            continue
        if max_budget and prop["price"] > max_budget:
            continue
        if property_type and property_type.lower() != prop["type"].lower():
            continue
        filtered.append(prop)
    return filtered
