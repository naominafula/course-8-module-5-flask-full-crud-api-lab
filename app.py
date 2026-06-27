from flask import Flask, jsonify, request

app = Flask(__name__)

class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    

    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    new_id = max([event.id for event in events]) + 1 if events else 1
    
    new_event = Event(new_id, data['title'])
    events.append(new_event)
    
    return jsonify(new_event.to_dict()), 201

@app.route('/events/<int:id>', methods=['PATCH'])
def update_event(id):
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    

    event = next((e for e in events if e.id == id), None)
    
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    

    event.title = data['title']
    
    return jsonify(event.to_dict()), 200

@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    global events
    
    event = next((e for e in events if e.id == id), None)
    
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events = [e for e in events if e.id != id]
    
    return jsonify({"message": f"Event {id} deleted successfully"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

@app.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event = next((e for e in events if e.id == id), None)
    
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    
    return jsonify(event.to_dict()), 200

if __name__ == "__main__":
    app.run(debug=True)