from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import sqlite3
from datetime import datetime
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import os

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS grocery_lists
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  created_date TEXT,
                  delivery_address TEXT,
                  items TEXT,
                  total_amount REAL)''')
    
    # Pre-populate some common grocery items
    c.execute('''CREATE TABLE IF NOT EXISTS common_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE,
                  default_price REAL)''')
    
    # Insert common items if they don't exist
    common_items = [
        ('Coconuts', 50.00),
        ('Rice (1kg)', 80.00),
        ('Wheat Flour (1kg)', 45.00),
        ('Sugar (1kg)', 60.00),
        ('Salt (1kg)', 25.00),
        ('Cooking Oil (1L)', 120.00),
        ('Onions (1kg)', 40.00),
        ('Potatoes (1kg)', 35.00),
        ('Tomatoes (1kg)', 55.00),
        ('Milk (1L)', 65.00),
        ('Eggs (12pcs)', 75.00),
        ('Bread', 35.00),
        ('Bananas (1kg)', 70.00),
        ('Apples (1kg)', 150.00),
        ('Chicken (1kg)', 280.00),
        ('Fish (1kg)', 320.00),
        ('Dal/Lentils (1kg)', 90.00),
        ('Tea Powder (250g)', 85.00),
        ('Coffee Powder (200g)', 120.00),
        ('Biscuits', 45.00)
    ]
    
    for item, price in common_items:
        c.execute('INSERT OR IGNORE INTO common_items (name, default_price) VALUES (?, ?)', (item, price))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_common_items')
def get_common_items():
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    c.execute('SELECT id, name, default_price FROM common_items ORDER BY name')
    items = [{'id': row[0], 'name': row[1], 'price': row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify(items)

@app.route('/update_common_item', methods=['POST'])
def update_common_item():
    data = request.json
    item_id = data.get('id')
    name = data.get('name')
    price = data.get('price')
    
    if not all([item_id, name, price]):
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    try:
        conn = sqlite3.connect('grocery.db')
        c = conn.cursor()
        c.execute('UPDATE common_items SET name = ?, default_price = ? WHERE id = ?', 
                  (name, float(price), item_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/delete_common_item', methods=['POST'])
def delete_common_item():
    data = request.json
    item_id = data.get('id')
    
    if not item_id:
        return jsonify({'success': False, 'message': 'Item ID required'})
    
    try:
        conn = sqlite3.connect('grocery.db')
        c = conn.cursor()
        c.execute('DELETE FROM common_items WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/add_common_item', methods=['POST'])
def add_common_item():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    
    if not all([name, price]):
        return jsonify({'success': False, 'message': 'Name and price required'})
    
    try:
        conn = sqlite3.connect('grocery.db')
        c = conn.cursor()
        c.execute('INSERT INTO common_items (name, default_price) VALUES (?, ?)', 
                  (name, float(price)))
        new_id = c.lastrowid
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'id': new_id})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/save_list', methods=['POST'])
def save_list():
    data = request.json
    
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO grocery_lists (created_date, delivery_address, items, total_amount)
                 VALUES (?, ?, ?, ?)''', 
              (data['date'], data['address'], json.dumps(data['items']), data['total']))
    
    list_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'list_id': list_id})

@app.route('/generate_pdf/<int:list_id>')
def generate_pdf(list_id):
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    c.execute('SELECT * FROM grocery_lists WHERE id = ?', (list_id,))
    grocery_list = c.fetchone()
    conn.close()
    
    if not grocery_list:
        return "List not found", 404
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.darkblue,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Build the PDF content
    story = []
    
    # Title
    title = Paragraph("Grocery Shopping List", title_style)
    story.append(title)
    
    # Date and Address info
    info_data = [
        ['Date:', grocery_list[1]],
        ['Delivery Address:', grocery_list[2] or 'Not specified']
    ]
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 20))
    
    # Items table
    items = json.loads(grocery_list[3])
    table_data = [['☐', 'Item', 'Quantity', 'Price (₹)', 'Total (₹)']]
    
    for item in items:
        table_data.append([
            '☐',
            item['name'],
            str(item['quantity']),
            f"₹{item['price']:.2f}",
            f"₹{item['total']:.2f}"
        ])
    
    # Add total row
    table_data.append(['', '', '', 'Grand Total:', f"₹{grocery_list[4]:.2f}"])
    
    table = Table(table_data, colWidths=[0.5*inch, 2.5*inch, 1*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Item names left-aligned
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    
    # Build PDF
    doc.build(story)
    
    # Prepare response
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=grocery_list_{list_id}.pdf'
    
    return response

@app.route('/view_saved_lists')
def view_saved_lists():
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    c.execute('SELECT id, created_date, delivery_address, total_amount FROM grocery_lists ORDER BY id DESC')
    lists = c.fetchall()
    conn.close()
    
    return render_template('saved_lists.html', lists=lists)

@app.route('/view_list/<int:list_id>')
def view_list(list_id):
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    c.execute('SELECT * FROM grocery_lists WHERE id = ?', (list_id,))
    grocery_list = c.fetchone()
    conn.close()
    
    if not grocery_list:
        return "List not found", 404
    
    items = json.loads(grocery_list[3])
    return render_template('view_list.html', grocery_list=grocery_list, items=items)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
