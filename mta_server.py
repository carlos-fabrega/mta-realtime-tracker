#!/usr/bin/env python3
from flask import Flask, render_template, jsonify
import requests
from google.transit import gtfs_realtime_pb2
import time

app = Flask(__name__)

FEED_URLS = {
    "ACE": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",
    "1234567": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs",
}

# Map of route and direction to destinations
ROUTE_DESTINATIONS = {
    # A train northbound
    'A_N': 'Inwood-207 St',
    # C train northbound  
    'C_N': '168 St',
    # 4 train northbound
    '4_N': 'Woodlawn',
    # 5 train northbound
    '5_N': 'Eastchester-Dyre',
}

def get_destination(route_id, direction):
    """Get destination based on route and direction"""
    key = f"{route_id}_{direction}"
    return ROUTE_DESTINATIONS.get(key, 'Uptown')

def fetch_mta_data(feed_url):
    try:
        response = requests.get(feed_url, timeout=10)
        response.raise_for_status()
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        return feed
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def parse_arrivals(feed, station_id_with_direction, route_filter=None):
    arrivals = []
    current_time = int(time.time())
    
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trip = entity.trip_update
            route_id = trip.trip.route_id
            
            if route_filter and route_id not in route_filter:
                continue
            
            for stop_update in trip.stop_time_update:
                stop_id = stop_update.stop_id
                
                if stop_id == station_id_with_direction:
                    if stop_update.HasField('arrival'):
                        arrival_time = stop_update.arrival.time
                    elif stop_update.HasField('departure'):
                        arrival_time = stop_update.departure.time
                    else:
                        continue
                    
                    minutes_away = int((arrival_time - current_time) / 60)
                    
                    if minutes_away >= 0:
                        direction_code = 'N' if stop_id[-1] == 'N' else 'S'
                        direction = 'Uptown' if direction_code == 'N' else 'Downtown'
                        destination = get_destination(route_id, direction_code)
                        
                        arrivals.append({
                            'route': route_id,
                            'minutes': minutes_away,
                            'direction': direction,
                            'destination': destination,
                            'time': arrival_time
                        })
    
    arrivals.sort(key=lambda x: x['time'])
    return arrivals

def get_all_trains():
    all_arrivals = []
    
    # Fetch A/C trains
    feed_ace = fetch_mta_data(FEED_URLS["ACE"])
    if feed_ace:
        arrivals_ac = parse_arrivals(feed_ace, "A38N", ["A", "C"])
        all_arrivals.extend(arrivals_ac)
    
    # Fetch 4/5 trains
    feed_numbered = fetch_mta_data(FEED_URLS["1234567"])
    if feed_numbered:
        arrivals_45 = parse_arrivals(feed_numbered, "635N", ["4", "5"])
        all_arrivals.extend(arrivals_45)
    
    all_arrivals.sort(key=lambda x: x['time'])
    return all_arrivals

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/trains')
def get_trains():
    trains = get_all_trains()
    return jsonify(trains)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
