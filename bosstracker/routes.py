import json

from flask import render_template, redirect, url_for, flash, request
from bosstracker import app, db
from bosstracker.forms import RegisterBossForm
from bosstracker.models import Boss
from sqlalchemy import func

def handle_death_change():
    change = request.json['deathChange']
    row_id = request.json['rowId']
    boss = Boss.query.filter_by(id=row_id).first()
    new_death_count = boss.deathcount + change

    if new_death_count >= 0:
        boss.deathcount = new_death_count
        db.session.commit()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def handle_name_change():
    change = request.json['newName']
    row_id = request.json['rowId']
    boss = Boss.query.filter_by(id=row_id).first()
    old_name = boss.bossname

    if change == old_name:
        return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}

    already_contained = Boss.query.filter_by(bossname=change).first()

    if already_contained:
        return json.dumps({'success': False, 'oldName': old_name}), 200, {'ContentType': 'application/json'}

    boss.bossname = change
    db.session.commit()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

def handle_remove_row():

    row_id = request.json['rowId']
    boss = Boss.query.filter_by(id=row_id).first()

    if not boss:
        return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}

    db.session.delete(boss)
    db.session.commit()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

def handle_completion_change():
    row_id = request.json['rowId']
    boss = Boss.query.filter_by(id=row_id).first()

    if not boss:
        return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}

    boss.iscompleted = request.json['iscompleted']
    db.session.commit()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/', methods=['GET', 'POST'])
def home():
    register_boss_form = RegisterBossForm()

    if register_boss_form.validate_on_submit():
        already_contained = Boss.query.filter_by(bossname=register_boss_form.bossname.data).first()

        if already_contained:
            flash('That boss already exists!', 'danger')
        else:
            boss = Boss(bossname=register_boss_form.bossname.data)
            db.session.add(boss)
            db.session.commit()
        all_bosses = Boss.query.all()
        total_deaths = db.session.query(func.sum(Boss.deathcount)).scalar()
        return render_template('data-display.html', title='Boss Tracker', form=register_boss_form, all_bosses=all_bosses, total_deaths=total_deaths)


    if request.json and request.method == 'POST' and 'deathChange' in request.json:
        return handle_death_change()

    if request.json and request.method == 'POST' and 'newName' in request.json:
        return handle_name_change()

    if request.json and request.method == 'POST' and 'remove' in request.json:
        return handle_remove_row()

    if request.json and request.method == 'POST' and 'iscompleted' in request.json:
        return handle_completion_change()

    all_bosses = Boss.query.all()
    total_deaths = db.session.query(func.sum(Boss.deathcount)).scalar()

    return render_template('data-display.html', title='Boss Tracker', form=register_boss_form, all_bosses=all_bosses, total_deaths=total_deaths)


