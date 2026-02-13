-- Create destinations database for tourism agent
-- Based on popular tourist destinations worldwide

CREATE TABLE IF NOT EXISTS destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    region TEXT,
    timezone TEXT,
    best_season TEXT,
    description TEXT,
    popular_activities TEXT
);

CREATE TABLE IF NOT EXISTS attractions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    category TEXT,
    description TEXT,
    estimated_duration_hours INTEGER
);

-- Insert popular destinations
INSERT INTO destinations (city, country, region, timezone, best_season, description, popular_activities) VALUES
('Tokyo', 'Japan', 'Asia', 'Asia/Tokyo', 'Spring (March-May), Fall (September-November)', 'Modern metropolis blending tradition and technology', 'Temples, Shopping, Cuisine, Cherry Blossoms'),
('Paris', 'France', 'Europe', 'Europe/Paris', 'Spring (April-June), Fall (September-October)', 'City of lights and romance', 'Museums, Architecture, Cuisine, Fashion'),
('New York', 'USA', 'North America', 'America/New_York', 'Spring (April-June), Fall (September-November)', 'The city that never sleeps', 'Museums, Broadway, Shopping, Dining'),
('London', 'UK', 'Europe', 'Europe/London', 'Late Spring (May-June), Early Fall (September)', 'Historic capital with royal heritage', 'Museums, History, Theatre, Parks'),
('Barcelona', 'Spain', 'Europe', 'Europe/Madrid', 'Spring (April-June), Fall (September-November)', 'Gaudi architecture and Mediterranean beaches', 'Architecture, Beaches, Cuisine, Nightlife'),
('Rome', 'Italy', 'Europe', 'Europe/Rome', 'Spring (April-June), Fall (September-October)', 'Ancient city with millennia of history', 'History, Architecture, Cuisine, Art'),
('Dubai', 'UAE', 'Middle East', 'Asia/Dubai', 'Winter (November-March)', 'Luxury and modern architecture in the desert', 'Shopping, Architecture, Desert Safari, Beaches'),
('Bangkok', 'Thailand', 'Asia', 'Asia/Bangkok', 'Winter (November-February)', 'Vibrant street life and ornate temples', 'Temples, Street Food, Markets, Nightlife'),
('Sydney', 'Australia', 'Oceania', 'Australia/Sydney', 'Spring (September-November), Fall (March-May)', 'Harbor city with iconic landmarks', 'Beaches, Opera House, Harbor, Wildlife'),
('Rio de Janeiro', 'Brazil', 'South America', 'America/Sao_Paulo', 'Fall (March-May), Winter (June-August)', 'Beaches, carnival, and Christ the Redeemer', 'Beaches, Carnival, Nature, Nightlife'),
('Istanbul', 'Turkey', 'Europe/Asia', 'Europe/Istanbul', 'Spring (April-May), Fall (September-November)', 'Bridge between East and West', 'History, Bazaars, Cuisine, Architecture'),
('Amsterdam', 'Netherlands', 'Europe', 'Europe/Amsterdam', 'Spring (April-May), Summer (June-August)', 'Canals, museums, and cycling culture', 'Museums, Canals, Cycling, Nightlife'),
('Singapore', 'Singapore', 'Asia', 'Asia/Singapore', 'Year-round (tropical climate)', 'Modern city-state with diverse culture', 'Gardens, Shopping, Cuisine, Architecture'),
('Cairo', 'Egypt', 'Africa', 'Africa/Cairo', 'Winter (October-April)', 'Ancient pyramids and pharaonic history', 'Pyramids, Museums, History, Nile Cruise'),
('Lisbon', 'Portugal', 'Europe', 'Europe/Lisbon', 'Spring (March-May), Fall (September-October)', 'Coastal capital with historic charm', 'History, Trams, Cuisine, Viewpoints');

-- Insert popular attractions
INSERT INTO attractions (name, city, country, category, description, estimated_duration_hours) VALUES
('Senso-ji Temple', 'Tokyo', 'Japan', 'Cultural', 'Ancient Buddhist temple in Asakusa', 2),
('Tokyo Skytree', 'Tokyo', 'Japan', 'Landmark', 'Tallest structure in Japan with observation decks', 2),
('Shibuya Crossing', 'Tokyo', 'Japan', 'Urban', 'World''s busiest pedestrian crossing', 1),
('Eiffel Tower', 'Paris', 'France', 'Landmark', 'Iconic iron lattice tower', 3),
('Louvre Museum', 'Paris', 'France', 'Museum', 'World''s largest art museum', 4),
('Notre-Dame Cathedral', 'Paris', 'France', 'Cultural', 'Medieval Catholic cathedral', 2),
('Statue of Liberty', 'New York', 'USA', 'Landmark', 'Symbol of freedom and democracy', 3),
('Central Park', 'New York', 'USA', 'Nature', 'Large public park in Manhattan', 3),
('Metropolitan Museum of Art', 'New York', 'USA', 'Museum', 'Largest art museum in the Americas', 4),
('Tower of London', 'London', 'UK', 'History', 'Historic castle and Crown Jewels', 3),
('British Museum', 'London', 'UK', 'Museum', 'World history and culture museum', 4),
('Buckingham Palace', 'London', 'UK', 'Landmark', 'Official residence of the British monarch', 2),
('Sagrada Familia', 'Barcelona', 'Spain', 'Cultural', 'Gaudi''s unfinished masterpiece', 3),
('Park Güell', 'Barcelona', 'Spain', 'Cultural', 'Colorful park designed by Gaudi', 2),
('La Rambla', 'Barcelona', 'Spain', 'Urban', 'Famous tree-lined pedestrian street', 2),
('Colosseum', 'Rome', 'Italy', 'History', 'Ancient Roman amphitheater', 3),
('Vatican Museums', 'Rome', 'Italy', 'Museum', 'Art and Christian history museums', 4),
('Trevi Fountain', 'Rome', 'Italy', 'Landmark', 'Baroque fountain and coin-tossing tradition', 1),
('Burj Khalifa', 'Dubai', 'UAE', 'Landmark', 'Tallest building in the world', 2),
('Dubai Mall', 'Dubai', 'UAE', 'Shopping', 'Largest shopping mall in the world', 4),
('Grand Palace', 'Bangkok', 'Thailand', 'Cultural', 'Former royal residence complex', 3),
('Wat Pho', 'Bangkok', 'Thailand', 'Cultural', 'Temple with giant reclining Buddha', 2),
('Sydney Opera House', 'Sydney', 'Australia', 'Landmark', 'Iconic performing arts center', 2),
('Bondi Beach', 'Sydney', 'Australia', 'Nature', 'Famous beach for surfing and swimming', 3),
('Christ the Redeemer', 'Rio de Janeiro', 'Brazil', 'Landmark', 'Iconic statue overlooking the city', 2),
('Copacabana Beach', 'Rio de Janeiro', 'Brazil', 'Nature', 'Famous beach with vibrant atmosphere', 4),
('Hagia Sophia', 'Istanbul', 'Turkey', 'History', 'Former church and mosque, now museum', 2),
('Grand Bazaar', 'Istanbul', 'Turkey', 'Shopping', 'One of the oldest covered markets', 3),
('Anne Frank House', 'Amsterdam', 'Netherlands', 'Museum', 'Historic house and biographical museum', 2),
('Van Gogh Museum', 'Amsterdam', 'Netherlands', 'Museum', 'Largest collection of Van Gogh artworks', 3),
('Gardens by the Bay', 'Singapore', 'Singapore', 'Nature', 'Futuristic nature park with Supertrees', 3),
('Marina Bay Sands', 'Singapore', 'Singapore', 'Landmark', 'Iconic hotel with rooftop infinity pool', 2),
('Pyramids of Giza', 'Cairo', 'Egypt', 'History', 'Ancient pyramids and the Sphinx', 4),
('Egyptian Museum', 'Cairo', 'Egypt', 'Museum', 'Vast collection of ancient Egyptian artifacts', 3),
('Belém Tower', 'Lisbon', 'Portugal', 'History', 'Fortified tower from the Age of Discoveries', 1),
('Jerónimos Monastery', 'Lisbon', 'Portugal', 'Cultural', 'Magnificent Manueline architecture', 2);

CREATE INDEX idx_destinations_city ON destinations(city);
CREATE INDEX idx_destinations_country ON destinations(country);
CREATE INDEX idx_attractions_city ON attractions(city);
CREATE INDEX idx_attractions_category ON attractions(category);
