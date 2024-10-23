from flask import Flask, render_template, request, redirect, url_for, session, flash
import datetime

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  # Necesaria para utilizar sesiones

# Inicializar la sesión para almacenar productos
@app.before_request
def initialize_session():
    if 'productos' not in session:
        session['productos'] = []

# Función para agregar un nuevo producto
def agregar_producto(producto):
    session['productos'].append(producto)
    session.modified = True

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para agregar un producto
@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto_view():
    if request.method == 'POST':
        nuevo_producto = {
            'id': request.form['id'],
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }
        
        # Verificar si el ID ya existe
        for producto in session['productos']:
            if producto['id'] == nuevo_producto['id']:
                flash('El ID del producto ya existe. Intenta con uno diferente.', 'error')
                return redirect(url_for('agregar_producto_view'))
        
        agregar_producto(nuevo_producto)
        flash('Producto agregado exitosamente.', 'success')
        return redirect(url_for('listar_productos'))
    
    return render_template('agregar_producto.html')

# Ruta para listar productos
@app.route('/listar_productos')
def listar_productos():
    productos = session['productos']
    return render_template('listar_productos.html', productos=productos)

# Ruta para eliminar un producto
@app.route('/eliminar_producto/<producto_id>', methods=['POST'])
def eliminar_producto(producto_id):
    session['productos'] = [p for p in session['productos'] if p['id'] != producto_id]
    session.modified = True
    flash('Producto eliminado exitosamente.', 'success')
    return redirect(url_for('listar_productos'))

if __name__ == '__main__':
    app.run(debug=True)