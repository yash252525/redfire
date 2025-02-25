from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class MealForm(FlaskForm):
    # Starter options
    starter = SelectField('Starter', choices=[
        ('', 'Select a starter...'),  # Default empty option
        ('soup', 'Soup of the Day'),
        ('salad', 'Caesar Salad'),
        ('bruschetta', 'Tomato Bruschetta')
    ], validators=[])

    # Main course options
    main_course = SelectField('Main Course', choices=[
        ('', 'Select a main course...'),  # Default empty option
        ('steak', 'Grilled Steak'),
        ('pasta', 'Spaghetti Carbonara'),
        ('salmon', 'Grilled Salmon')
    ], validators=[])

    # Dessert options
    dessert = SelectField('Dessert', choices=[
        ('', 'Select a dessert...'),  # Default empty option
        ('cake', 'Chocolate Cake'),
        ('ice_cream', 'Vanilla Ice Cream'),
        ('fruit', 'Fresh Fruit Salad')
    ], validators=[])

    submit = SubmitField('Submit Order')