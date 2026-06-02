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
@bp.route('/api/rooms', methods=['GET'])
def get_rooms():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
    conn.close()
    return jsonify({"items": rooms, "count": len(rooms)})

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

# TODO: 개별 조회, 수정(PUT), 삭제(DELETE) 루틴도 구조에 맞춰 추가 구현

# ----------------------------------------
# 예약 API
# ----------------------------------------
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