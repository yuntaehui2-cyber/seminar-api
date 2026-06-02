from flask import Blueprint, request, jsonify
from app.db import get_db_connection

bp = Blueprint('api', __name__)

# ----------------------------------------
# 헬스체크 API
# ----------------------------------------
@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

# ----------------------------------------
# 세미나룸 API (CRUD)
# ----------------------------------------
# 1. 세미나룸 전체 조회
@bp.route('/api/rooms', methods=['GET'])
def get_rooms():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
    conn.close()
    return jsonify({"items": rooms, "count": len(rooms)})

# 2. 세미나룸 단건(상세) 조회 - [추가됨]
@bp.route('/api/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM rooms WHERE id = %s", (room_id,))
        room = cursor.fetchone()
    conn.close()
    if not room:
        return jsonify({"message": "Room not found"}), 404
    return jsonify(room)

# 3. 세미나룸 생성
@bp.route('/api/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = "INSERT INTO rooms (name, capacity, equipment) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data['name'], data['capacity'], data.get('equipment')))
        room_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"id": room_id, "message": "created"}), 201

# 4. 세미나룸 수정 - [추가됨]
@bp.route('/api/rooms/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    data = request.get_json()
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = "UPDATE rooms SET name = %s, capacity = %s, equipment = %s WHERE id = %s"
        cursor.execute(sql, (data['name'], data['capacity'], data.get('equipment'), room_id))
    conn.commit()
    conn.close()
    return jsonify({"id": room_id, "message": "updated"})

# 5. 세미나룸 삭제 - [추가됨]
@bp.route('/api/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
    conn.commit()
    conn.close()
    return jsonify({"id": room_id, "message": "deleted"})


# ----------------------------------------
# 예약 API
# ----------------------------------------
# 1. 예약 목록 조회 (필터 지원)
@bp.route('/api/reservations', methods=['GET'])
def get_reservations():
    room_id = request.args.get('room_id')
    date = request.args.get('date')
    
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM reservations WHERE 1=1"
        params = []
        if room_id:
            sql += " AND room_id = %s"
            params.append(room_id)
        if date:
            sql += " AND date = %s"
            params.append(date)
        cursor.execute(sql, params)
        reservations = cursor.fetchall()
    conn.close()
    return jsonify({"items": reservations, "count": len(reservations)})

# 2. 예약 생성
@bp.route('/api/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = """INSERT INTO reservations 
                 (room_id, user_name, user_email, date, start_time, end_time, purpose) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (
            data['room_id'], data['user_name'], data['user_email'],
            data['date'], data['start_time'], data['end_time'], data.get('purpose')
        ))
        res_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"id": res_id, "message": "reserved"}), 201

# 3. 예약 취소(삭제) - [추가됨]
@bp.route('/api/reservations/<int:res_id>', methods=['DELETE'])
def delete_reservation(res_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM reservations WHERE id = %s", (res_id,))
    conn.commit()
    conn.close()
    return jsonify({"id": res_id, "message": "cancelled"})