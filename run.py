from app import create_app

app = create_app()

if __name__ == '__main__':
    # Запуск приложения с включенным режимом отладки и на определенном порту
    app.run(debug=True)
