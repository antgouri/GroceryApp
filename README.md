# GroceryApp
A Grocery check list app based on Python and Flask
# 🛒 Grocery Checklist & Purchase App

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A comprehensive web-based grocery shopping list application built with Flask and Python. Create, manage, and track your grocery shopping with features like PDF export, real-time calculations, and persistent storage.

![Grocery App Demo](https://via.placeholder.com/800x400/28a745/ffffff?text=Grocery+Checklist+App+Demo)

## ✨ Features

### 🎯 Core Functionality
- **📅 Real-time Date & Time Display** - Always know when your list was created
- **📝 Custom Item Entry** - Add any grocery item with custom prices
- **⚡ Quick Add Common Items** - Pre-loaded with 20+ common groceries
- **💰 Auto-calculated Pricing** - Real-time totals and grand total
- **✅ Interactive Checklist** - Check off items as you shop
- **📄 PDF Export & Print** - Professional shopping lists for offline use
- **🗄️ Database Storage** - All lists saved for future reference
- **📍 Delivery Address** - Add delivery location details

### 🔧 Management Features
- **✏️ Edit Common Items** - Customize item names and default prices
- **➕ Add New Common Items** - Build your personalized quick-add library
- **🗑️ Delete Items** - Remove unwanted common items
- **📊 Shopping Progress** - Visual progress tracking while shopping
- **📱 Responsive Design** - Works perfectly on mobile and desktop
- **🔍 Shopping History** - View and reprint previous lists

## 🚀 Demo

Try the live demo: [Coming Soon](#)

Or see screenshots:

| Main Interface | Edit Common Items | PDF Export |
|---|---|---|
| ![Main](https://via.placeholder.com/250x150/007bff/ffffff?text=Main+Interface) | ![Edit](https://via.placeholder.com/250x150/28a745/ffffff?text=Edit+Items) | ![PDF](https://via.placeholder.com/250x150/dc3545/ffffff?text=PDF+Export) |

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- Flask

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/grocery-checklist-app.git
   cd grocery-checklist-app
   ```

2. **Create a virtual / conda environment** (recommended)
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
    OR

   ```bash
   conda create -n grocery python==3.10

   conda activate grocery

   #pip commands follow here
   pip install <lib>

   #once complete 
   conda deactivate
   ```
   

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   ```
   http://localhost:5000
   ```

## 🏗️ Project Structure

```
grocery-checklist-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── LICENSE               # MIT License
├── grocery.db            # SQLite database (auto-created)
└── templates/            # HTML templates
    ├── base.html         # Base template with common layout
    ├── index.html        # Main application interface
    ├── saved_lists.html  # View saved grocery lists
    └── view_list.html    # Individual list details
```

## 💡 Usage

### Creating Your First List

1. **Add Items**: Use quick-add buttons or enter custom items
2. **Set Quantities**: Adjust quantities for each item
3. **Add Address**: Enter delivery location (optional)
4. **Save List**: Save to database for future reference

### Managing Common Items

1. **Edit Mode**: Click "Edit Items" to modify common items
2. **Customize**: Edit names and prices to match your local market
3. **Add New**: Create custom common items for faster shopping
4. **Delete**: Remove items you don't use

### While Shopping

1. **Check Off Items**: Tap checkboxes as you shop
2. **Track Progress**: Watch the progress bar fill up
3. **Print/PDF**: Get offline copies for shopping

## 🔧 Configuration

### Database Setup

The app uses SQLite by default. To use MySQL:

1. Install MySQL connector:
   ```bash
   pip install mysql-connector-python
   ```

2. Update database configuration in `app.py`:
   ```python
   # Replace SQLite connection with MySQL
   import mysql.connector
   
   def get_db_connection():
       return mysql.connector.connect(
           host='localhost',
           user='your_username',
           password='your_password',
           database='grocery_db'
       )
   ```

### Customizing Common Items

Edit the pre-loaded items in `app.py`:

```python
common_items = [
    ('Your Local Item', 25.00),
    ('Another Item', 45.50),
    # Add more items here
]
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main application interface |
| `GET` | `/get_common_items` | Fetch all common items |
| `POST` | `/save_list` | Save grocery list to database |
| `POST` | `/update_common_item` | Update existing common item |
| `POST` | `/add_common_item` | Add new common item |
| `POST` | `/delete_common_item` | Delete common item |
| `GET` | `/generate_pdf/<id>` | Generate PDF for specific list |
| `GET` | `/view_saved_lists` | View all saved lists |
| `GET` | `/view_list/<id>` | View specific list details |

## 🧪 Testing

Run the application in debug mode:

```bash
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development     # Windows
python app.py
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update README for new features
- Test thoroughly before submitting

## 📋 TODO / Roadmap

- [ ] User authentication and multi-user support
- [ ] Barcode scanning integration
- [ ] Shopping list sharing functionality
- [ ] Mobile app (React Native/Flutter)
- [ ] Integration with online grocery stores
- [ ] Recipe-to-shopping-list conversion
- [ ] Shopping analytics and insights
- [ ] Dark mode theme
- [ ] Multi-language support
- [ ] Voice input for items

## 🐛 Known Issues

- PDF generation may take a few seconds for large lists
- Mobile browsers may have slight layout differences
- Some older browsers may not support all features

## 📱 Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 80+ | ✅ Fully Supported |
| Firefox | 75+ | ✅ Fully Supported |
| Safari | 13+ | ✅ Fully Supported |
| Edge | 80+ | ✅ Fully Supported |
| IE | Any | ❌ Not Supported |

## 📊 Performance

- **Load Time**: < 2 seconds
- **PDF Generation**: < 5 seconds
- **Database Operations**: < 100ms
- **Mobile Performance**: Optimized for 3G networks

## 🔒 Security

- Input validation on all forms
- SQL injection protection
- XSS prevention
- CSRF protection (recommended for production)
- No sensitive data stored in cookies

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Ananth G S**
- GitHub: [https://github.com/antgouri]
- Email: devified.ananth@gmail.com

## 🙏 Acknowledgments

- Flask team for the excellent web framework
- ReportLab for PDF generation capabilities
- Bootstrap for responsive UI components
- Font Awesome for beautiful icons
- SQLite for lightweight database solution

## 💖 Support

If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 📝 Contributing to documentation
- 💰 [Buy me a coffee](https://buymeacoffee.com/yourusername)

---

<div align="center">

**[⬆ Back to Top](#-grocery-checklist--purchase-app)**

Made with ❤️ by [Your Name](https://github.com/yourusername)

</div>
