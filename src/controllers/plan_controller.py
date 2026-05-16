from flask import render_template, request, jsonify
from app import app
import re

from models.event_model import EventModel
from models.bookings_model import BookingModel

@app.route("/plan", methods=['GET', 'POST'])
def plan():
    if request.method == "POST":
        name = request.form.get('user_name', "").strip()
        phone = request.form.get('user_phone', "").strip()
        email = request.form.get('user_email', "").strip()
        date_str = request.form.get('date', '').strip()
        time_slot = request.form.get('time_slot', "").strip()
        comment = request.form.get('comment', "").strip()

        if len(name) < 3:
            return jsonify({"status": "error", "errors": "имя должно содержать хотя бы 3 символа"}), 400
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return jsonify({"status": "error", "errors": "Неверный email"}), 400
        if not date_str:
            return jsonify({"status": "error", "errors": "Выберите дату встречи"}), 400

        event = EventModel.get_by_date(date_str)
        if not event:
            return jsonify({"status": "error", "errors": "Событие на эту дату не найдено!"}), 404

        BookingModel.create(
            event_id=event['id'],
            user_name=name,
            user_phone=phone,
            user_email=email,
            time_slot=time_slot,
            comment=comment
        )
        print(f'- запись сохранена: {name} на {date_str} {time_slot}')
        return jsonify({"status": "ok"})

    # GET-запрос
    events = EventModel.get_all()
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