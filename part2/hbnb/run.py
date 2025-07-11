from app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the app in development mode
    app.run(debug=True, host='0.0.0.0', port=5000)