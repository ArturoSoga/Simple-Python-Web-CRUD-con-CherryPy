import cherrypy

class GridApp:
    def __init__(self):
        self.dataEmployes = [
            {"id": 1, "nombre": "Juan", "edad": 25,"puesto":"Contador","fechaIngreso":"2023-05-14"},
            {"id": 2, "nombre": "Ana", "edad": 30,"puesto":"Operador","fechaIngreso":"2021-01-19"},
            {"id": 3, "nombre": "Luis", "edad": 22,"puesto":"Administrado","fechaIngreso":"2021-01-19"},
            {"id": 4, "nombre": "Maria", "edad": 28,"puesto":"Analista","fechaIngreso":"2018-09-03"}
            ]
        self.current_id = None
        
    @cherrypy.expose
    def index(self):
        return self.generate_grid()

    @cherrypy.expose
    def add_employee(self,id,nombre,edad,puesto,fechaIngreso):
        newEmpl = len(self.dataEmployes) + 1
        self.dataEmployes.append({"id": newEmpl, "nombre": nombre, "edad": edad,"puesto":puesto,"fechaIngreso":fechaIngreso})
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def edit_employee(self,id,nombre,edad,puesto,fechaIngreso):
        for empl in self.dataEmployes:
            if empl['id'] == int(id):
                empl['nombre'] = nombre
                empl['edad'] = int(edad)
                empl['puesto'] = puesto
                empl['fechaIngreso'] = fechaIngreso
                break
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def delete_employee(self, id):
        self.dataEmployes = [emp for emp in self.dataEmployes if emp['id'] != int(id)]
        raise cherrypy.HTTPRedirect('/')
    
    def generate_grid(self):
        html = """
        <html>
        <head>
            <title>CRUD con CherryPy</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
            <script>
                function openModal() {
                    clearForm()
                    document.getElementById('myModal').style.display = 'block';
                }
                function closeModal() {
                    document.getElementById('myModal').style.display = 'none';
                }
                window.onclick = function(event) {
                    if (event.target == document.getElementById('myModal')) {
                        closeModal();
                    }
                }

                function openEditModal(id, nombre, edad, puesto, fechaIngreso) {
                    document.getElementById('employeeId').value = id;
                    document.getElementById('employeeName').value = nombre;
                    document.getElementById('employeeAge').value = edad;
                    document.getElementById('employeeposition').value = puesto;
                    document.getElementById('employeeEntryDate').value = fechaIngreso;
                    document.getElementById('employeeForm').action = 'edit_employee';
                    $('#myModal').modal('show'); // Mostrar el modal
                }

                 function clearForm() {
                    document.getElementById('employeeForm').reset();
                    document.getElementById('employeeForm').action = 'add_employee';
                }
            </script>
             <style>
                table {
                    width: 90%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
           <div class="content center m-5" >
           <div class="m-2 p-2">
            <h2>Empleados</h2>
            <div>
           </div>

            <div class="container">
             <div class="row">
              <div class="col text-center">
                <table class=" m-3 " >
                    <tr>
                        <th>No. Empleado</th>
                        <th>Nombre</th>
                        <th>Edad</th>
                        <th>Puesto</th>
                        <th>Fecha Ingreso</th>
                        <th>Acciones</th>
                    </tr>
        """

        for item in self.dataEmployes :
            html += f"""
                <tr>
                    <td>{item['id']}</td>
                    <td>{item['nombre']}</td>
                    <td>{item['edad']}</td>
                    <td>{item['puesto']}</td>
                    <td>{item['fechaIngreso']}</td>
                    <td>
                        <button class="btn btn-warning" onclick="openEditModal( {item['id']}, '{item['nombre']}', {item['edad']} , '{item['puesto']}' , '{item['fechaIngreso']}' )">Editar</button>
                        <a href="delete_employee?id={item['id']}" class="btn btn-danger" onclick="return confirm('¿Estás seguro de que deseas eliminar este empleado?');">Eliminar</a>
                    </td>
                </tr>
            """

        html += """
                </table>
               </div>
             </div>
            </div>


            
            <div class="container">
             <div class="row">
              <div class="col text-center">
              <button onclick="clearForm()" class="btn btn-primary" data-toggle="modal" data-target="#myModal">Agregar Empleado</button>
              </div>
             </div>
            </div>

            <!-- Modal -->
             <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="modalTitle" >Agregar/Editar Empleado</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <form id="employeeForm" method="post" action="add_employee">
                            
                                <input type="hidden" name="id" id="employeeId">
                                
                                <div class="form-group">
                                    <label for="nombre">Nombre</label>
                                    <input type="text" class="form-control" name="nombre" id="employeeName" required>
                                </div>
                                
                                <div class="form-group">
                                    <label for="edad">Edad</label>
                                    <input type="number" class="form-control" name="edad" id="employeeAge" required>
                                </div>
                                
                                <div class="form-group">
                                    <label for="puesto">puesto</label>
                                    <input type="text" class="form-control" name="puesto" id="employeeposition" required>
                                </div>

                                <div class="form-group">
                                    <label for="fechaIngreso">Fecha Ingreso</label>
                                    <input type="date" class="form-control" name="fechaIngreso" id="employeeEntryDate" required>
                                </div>

                                <div class="container">
                                  <div class="row">
                                    <div class="col text-center">
                                <button type="submit" class="btn btn-primary">Guardar</button>
                                </div>
                                </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return html

if __name__ == '__main__':
    cherrypy.quickstart(GridApp())
