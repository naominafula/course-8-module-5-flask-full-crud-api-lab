from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    location = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location
        }

with app.app_context():
    db.create_all()
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Missing required fields"}), 400
        
    new_event = Event(
        title=data['title'],
        description=data.get('description', ''),
        location=data.get('location', '')
    )
    db.session.add(new_event)
    db.session.commit()
    
    return jsonify(new_event.to_dict()), 201
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events]), 200
@app.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.to_dict()), 200
@app.route('/events/<int:id>', methods=['PATCH', 'PUT'])
def update_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
        
    data = request.get_json()
    if 'title' in data:
        event.title = data['title']
    if 'description' in data:
        event.description = data['description']
    if 'location' in data:
        event.location = data['location']
        
    db.session.commit()
    return jsonify(event.to_dict()), 200
@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
        
    db.session.delete(event)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5555)