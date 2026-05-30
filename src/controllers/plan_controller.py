from flask import render_template, request, jsonify
from injector import inject
from app import app

from models.event_model import EventModel
from models.bookings_model import BookingModel
from db.db import Database

@app.route("/plan", methods=['GET', 'POST'])
@inject  #
def plan(event_model: EventModel, db: Database):
    if request.method == "POST":
        name = request.form.get('user_name', "").strip()
        phone = request.form.get('user_phone', "").strip()
        email = request.form.get('user_email', "").strip()
        date_str = request.form.get('date', '').strip()
        time_slot = request.form.get('time_slot', "").strip()
        comment = request.form.get('comment', "").strip()
        print(f'- получены данные: {name}, {phone}, {email}, {date_str}, {time_slot}, {comment}')

        event = event_model.get_by_date(date_str)
        if event is None:
            return jsonify({"status": "error", "errors": "Событие на эту дату не найдено!"}), 404
        print("Событие:", event)
              
        try:
            booking_model = BookingModel(
                db=db,
                event_id=None,
                user_name=name,
                user_email=email,
                user_phone=phone or None,
                time_slot=time_slot or None,
                comment=comment or None
            )
            print("Объект бронирования создан")
        except ValueError as e:
            return jsonify({'status': 'error', 'errors': str(e)}), 400
        
        try:
            event = EventModel.get_by_date(date_str)
            if event is None:
                return jsonify({"status": "error", "errors": "Событие на эту дату не найдено!"}), 404
            
            booking_model.event_id = event.id
        except Exception as e:
            return jsonify({"status": "error", "errors": f"ошибка при поиске события: {str(e)}"}), 500
        
        if booking_model.save():
            print(f'- запись сохранена: {name} на {date_str} {time_slot}')
            return jsonify({"status": "ok"})
        
        else: 
            return jsonify({"status": "error", "errors": "Не удалось сохранить бронирование"}), 500

    # GET-запрос
    events = event_model.get_all()
    events_by_date = {}
    for ev in events:
        # Преобразуем дату в строку ISO
        date_val = ev['event_date']
        if hasattr(date_val, 'isoformat'):
            date_iso = date_val.isoformat()
        else:
            date_iso = str(date_val)
        book_info = f"«{ev['book_title']}» {ev['book_author']}"
        events_by_date.setdefault(date_iso, []).append(book_info)

    return render_template("plan.html", services=events_by_date)