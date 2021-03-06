import pymysql
from .Amigo import Amigo
from .Post import Post
from .Multimedia import Multimedia
from .Pagina_participa import Pagina_participa
from .Grupo_participa import Grupo_participa
from .Chat import Chat
import hashlib
from datetime import date
from pathlib import Path

class Usuario (object):
    id_usuario = None
    formacion_empleo = []
    lugares_vividos = []
    informacion_basica = None
    acontecimientos_importantes = []
    nombre = None
    apellido = None
    correo_electronico = None
    numero_tarjeta_credito = None
    fecha_vencimiento_tarjeta = None
    codigo_seguridad_tarjeta = None
    fecha_nacimiento = None
    genero_sexual = None
    contrasena_hash = None
    paginas = []
    grupos = []
    amigos = []


    def crear_usuario (self , formacion_empleo , lugares_vividos , informacion_basica #ANDA
                       , acontecimientos_importantes , nombre , apellido , correo_electronico , numero_tarjeta_credito
                       , fecha_vencimiento_tarjeta , codigo_seguridad_tarjeta , fecha_nacimiento , genero_sexual
                       , contrasena_hash , db):

        cursor = db.cursor(pymysql.cursors.DictCursor)

        cursor.execute("select correoelectronico from usuario")
        check = cursor.fetchall()

        for item in check:
            if item["correoelectronico"] == correo_electronico:
                return 0 , "el correo esta en uso"

        contrasena_hash = self.hashear_contrasena(contrasena_hash)
        cursor.execute("insert into Usuario values (NULL , '"+str(formacion_empleo)+"' , '"+str(lugares_vividos)+"' "
                       ", '"+str(informacion_basica)+"' , '"+str(acontecimientos_importantes)+"' , '"+str(nombre)+"' "
                       ", '"+str(apellido)+"' , '"+str(correo_electronico)+"' , '"+str(numero_tarjeta_credito)+"'"
                       ", '"+str(fecha_vencimiento_tarjeta)+"' , '"+str(codigo_seguridad_tarjeta)+"' , '"+str(fecha_nacimiento)+"'"
                       " , '"+str(genero_sexual)+"' , '"+str(contrasena_hash)+"')")

        id = cursor.lastrowid

        self.id_usuario = id
        self.formacion_empleo = self.crear_lista(formacion_empleo)
        self.lugares_vividos = self.crear_lista(lugares_vividos)
        self.informacion_basica = informacion_basica
        self.acontecimientos_importantes = self.crear_lista(acontecimientos_importantes)
        self.nombre = nombre
        self.apellido = apellido
        self.correo_electronico = correo_electronico
        self.numero_tarjeta_credito = numero_tarjeta_credito
        self.fecha_vencimiento_tarjeta = fecha_vencimiento_tarjeta
        self.codigo_seguridad_tarjeta = codigo_seguridad_tarjeta
        self.fecha_nacimiento = fecha_nacimiento
        self.genero_sexual = genero_sexual
        self.contrasena_hash = contrasena_hash

        return self

    def eliminar_usuario (self , db): #TERMIANR DE HACER Y TESTEAR
        cursor = db.cursor(pymysql.cursors.DictCursor)

        cursor.execute("select idamigo from usuario_has_usuario where usuario_idusuario = "
                       "'"+str(self.id_usuario)+"' or usuario_idusuario1 = '"+str(self.id_usuario)+"'")
        id = cursor.fetchall()
        if id != ():
            for item in id:
                cursor.execute("delete from chat where usuario_has_usuario.idamigo = '"+str(item["idamigo"])+"'")
                cursor.execute("delete from usuario_has_usuario where id_amigo = '" + str(item["idamigo"]) + "'")

        cursor.execute("select idgrupo from grupo where usuario_idusuario = '" + str(self.id_usuario) + "'")
        id = cursor.fetchall()

        if id != ():
            for item in id:
                cursor.execute(
                    "select usuario_idusuario , administrador from grupoparticipa where grupo_idgrupo = '" + str(
                        item["idgrupo"]) + "'")
                datos = cursor.fetchall()

                if (len(datos) == 1):
                    cursor.execute("delete from grupoparticipa where usuario_idusuario = '" + str(item[self.id_usuario]) + "'")
                    cursor.execute("delete from grupo where idgrupo = '" + str(item["idgrupo"]) + "'")
                else:
                    for item2 in datos:
                        if str(item2["administrador"]) == "1":
                            cursor.execute("update grupo set usuario_idusuario = "
                                           "'" + str(item2["usuario_idusuario"]) + "' where id_grupo = '" + str(
                                item["idgrupo"]) + "'")
                        break

        cursor.execute("select idpagina from pagina where usuario_idusuario = '" + str(self.id_usuario) + "'")
        id = cursor.fetchall()

        if id != ():
            for item in id:
                cursor.execute("select usuario_idusuario , administrador from paginaparticipa where pagina_idpagina = '" + str(
                        item["idpagina"]) + "'")
                datos = cursor.fetchall()

                if datos == ():
                    cursor.execute("delete from pagina where idpagina = '" + str(item["idpagina"]) + "'")
                else:
                    for item2 in datos:
                        if str(item2["administrador"]) == "1":

                            cursor.execute("update pagina set usuario_idusuario = "
                                           "'" + str(item2["usuario_idusuario"]) + "' where id_pagina = '" + str(
                                item["idpagina"]) + "'")
                        break

        cursor.execute("select idmultimedia from multimedia where usuario_idusuario = '" + str(self.id_usuario) + "'")
        id = cursor.fetchall()

        if id != ():
            for item in id:
                cursor.execute("delete from post_has_multimedia where pagina_idpagina = '" + str(item["idmultimedia"]) + "'")
                cursor.execute("delete from post where multimedia_idmultimedia = '" + str(item["idmultimedia"]) + "'")
                cursor.execute("delete from multimedia where idmultimedia = '" + str(item["idmultimedia"]) + "'")

        cursor.execute("delete from usuario where idusuario = '" + str(self.id_usuario) + "'")



    def hashear_contrasena (self , contrasena):
        return hashlib.md5(contrasena.encode('utf-8')).hexdigest()

    def crear_lista (self , dato):
        datos = []
        datos = dato.split(",")
        return datos

    def loguear (self , correo , contrasena , db):

        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select CorreoElectronico from Usuario")
        datos = cursor.fetchall()

        for item in datos:
            if item["CorreoElectronico"] == correo:
                cursor.execute("select contrasena_hash from Usuario where CorreoElectronico = '"+str(correo)+"'")
                datos = cursor.fetchall()

                if datos[0]["contrasena_hash"] == self.hashear_contrasena(contrasena):
                    return 1
        return 0

    def agregar_amigo(self , id_amigo, db):
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select idusuario from Usuario")
        correo = cursor.fetchall()
        for item in correo:
            if item["idusuario"] == id_amigo:
                cursor.execute("select * from usuario_has_usuario")
                datos = cursor.fetchall()
                for item in datos:

                    if (((item["usuario_idusuario"] == self.correo_electronico) and
                            (item["usuario_idusuario1"] == id_amigo) and (str(item["estado"]) == "0")) or
                            ((item["usuario_idusuario"] == id_amigo) and
                            (item["usuario_idusuario1"] == self.correo_electronico) and (str(item["estado"]) == "0"))):
                            return 0

                cursor.execute("insert into usuario_has_usuario values (NULL , '" + str(self.id_usuario) + "' "
                               ", '" + str(id_amigo) + "' , '" + "0" + "')")
                return 1
        return 0

    def eliminar_amigo(self , id_amigo , db):
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select * from usuario_has_usuario")
        datos = cursor.fetchall()
        for item in datos:
            if (((str(item["usuario_idUsuario"]) == str(self.id_usuario)) and (str(item["usuario_idUsuario1"])
                == str(id_amigo))) or ((str(item["usuario_idIsuario"]) == str(id_amigo))
                and (str(item["usuario_idUsuario1"]) == str(self.id_usuario)))):
                cursor.execute("delete from usuario_has_usuario where IdAmigo = '" + str(item["IdAmigo"]) + "'")
                return 1

        return 0 , "no son amigos"

    def subir_multimedia (self , archivo , creacion , album , db): #TERMINAR
        cursor = db.cursor(pymysql.cursors.DictCursor)
        mi_multimedia = Multimedia()
        #terminar
        cursor.execute("insert into Multimedia values (NULL , )")
        return 1

    def crear_post (self , fecha  , descripcion , id_pagina , id_grupo , id_multimedia , db): #ANDA
        cursor = db.cursor(pymysql.cursors.DictCursor)

        if id_pagina == 0 and id_grupo != 0:
            cursor.execute("insert into Post values (NULL , '" + str(fecha) + "' , '" + str(descripcion) + "' ,"
                           "NULL ,  '" + str(id_grupo) + "'  , '" + str(self.id_usuario) + "' , 0)")
        elif id_pagina != 0 and id_grupo == 0:
            cursor.execute("insert into Post values (NULL , '" + str(fecha) + "' , '" + str(descripcion) + "' ,"
                           " '" + str(id_pagina) + "' , NULL , '" + str(self.id_usuario) + "' , 0)")
        else:
            cursor.execute("insert into Post values (NULL , '" + str(fecha) + "' , '" + str(descripcion) + "' ,"
                           " NULL , NULL , '" + str(self.id_usuario) + "' , 0)")
        return 1

        def eliminar_post (self , id_post , db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("select grupo_idgrupo , pagina_idpagina from post where idpost = '"+str(id_post)+"'")
            check = cursor.fetchall()

            if (check != ()):
                if str(check[0]["grupo_idgrupo"]) != '':
                    cursor.execute("select usuario_idusuario from grupoparticipa where grupo_idgrupo = "
                                   "'"+str(str(check[0]["grupo_idgrupo"]))+"'")
                    id = cursor.fetchall()
                    id = id[0]["usuario_idusuario"]
                    if id == self.id_usuario:
                        cursor.execute("delete from post where idpost = '"+str(id_post)+"'")
                        return 1

                elif str(check[0]["pagina_idpagina"]) != '':
                    cursor.execute("select usuario_idusuario from paginaparticipa where pagina_idpagina = "
                                   "'"+str(str(check[0]["pagina_idpagina"]))+"'")
                    id = cursor.fetchall()
                    id = id[0]["usuario_idusuario"]
                    if id == self.id_usuario:
                        cursor.execute("delete from post where idpost = '"+str(id_post)+"'")
                        return 1
                else:
                    cursor.execute("select usuario_idusuario from post where idpost")
                    id = cursor.fetchall()
                    id = id[0]["usuario_idusuario"]
                    if (id == self.id_usuario):
                        cursor.execute("delete from post where idpost = '"+str(id_post)+"'")
                        return 1
            return 0

    def mandar_mensaje (self , id_amigo , mensaje , fecha , db):
        cursor = db.cursor(pymysql.cursors.DictCursor)

        cursor.execute("select estado from usuario_has_usuario where idamigo = '" + str(id_amigo) + "'")
        check = cursor.fetchall()
        check = check[0]["estado"]
        if check == 2:
            return 0

        cursor.execute("select usuario_idUsuario from usuario_has_usuario where IdAmigo = '" + str(id_amigo) + "'")
        usuario_id = cursor.fetchall()
        usuario_id = usuario_id[0]["usuario_idUsuario"]
        if usuario_id == self.id_usuario:
            emisor = 1
        else:
            emisor = 0

        cursor.execute("insert into Chat values(NULL , '" + str(mensaje) + "' , '" + str(id_amigo) + "' , "
                       "'" + str(fecha) + "' , '" + str(emisor) + "')")
        return 1

    def suscribir_pagina (self , id_pagina , db):
        cursor = db.cursor(pymysql.cursors.DictCursor)

        for item in self.lista_paginas:
            if item.usuario_idusuario == self.id_usuario and item.id_pagina == id_pagina:
                return 0;

        cursor.execute("insert into paginaparticipa values (NULL , '" + str(id_pagina) + "' , '" + "0" + "' , '" + str(
            self.id_usuario) + "')")
        return 1

    def suscribir_grupo (self , id_grupo , db):
        cursor = db.cursor(pymysql.cursors.DictCursor)

        for item in self.lista_grupos:
            if item.usuario_idUsuario == self.id_usuario and item.id_grupo == id_grupo:
                return 0;

        cursor.execute("insert into grupoparticipa values (NULL , '" + "0" + "' , "
                       "'" + str(self.id_usuario) + "' , '" + str(id_grupo) + "' , '" + "0" + "')")
        return 1

        def desuscribir_pagina(self, id_pagina, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("delete from paginaparticipa where idPagina = '" + str(id_pagina) + "' and usuario_idUsuario = '" + str(self.id_usuario) + "'")
            return 0

        def desuscribir_grupo(self, id_grupo, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("delete from grupoparticipa where idGrupo = '" + str(id_grupo) + "' and usuario_idusuario = '" + str(self.id_usuario) + "'")
            return 1

        def dar_like(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("insert into like values ('" + str(self.id_usuario) + "' , '" + str(id_post) + "')")
            return 1

        def sacar_like(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("delete from like where usuario_idusuario = '" + str(self.id_usuario) + "'"
                           " and post_idpost '" + str(id_post) + "')")
            return 1

        def dar_dislike(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("insert into dislike values ('" + str(self.id_usuario) + "' , '" + str(id_post) + "')")
            return 1

        def sacar_dislike(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("delete from dislike where usuario_idusuario = '" + str(self.id_usuario) + "'"
                           " and post_idpost '" + str(id_post) + "')")
            return 1

        def dar_anger(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("insert into anger values ('" + str(self.id_usuario) + "' , '" + str(id_post) + "')")
            return 1

        def sacar_anger(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("delete from anger where usuario_idusuario = '" + str(self.id_usuario) + "'"
                           " and post_idpost '" + str(id_post) + "')")
            return 1

        def dar_sad(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("insert into sad values ('" + str(self.id_usuario) + "' , '" + str(id_post) + "')")
            return 1

        def sacar_sad(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("delete from sad where usuario_idusuario = '" + str(self.id_usuario) + "'"
                           " and post_idpost '" + str(id_post) + "')")
            return 1

        def dar_wow(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("insert into wow values ('" + str(self.id_usuario) + "' , '" + str(id_post) + "')")
            return 1

        def sacar_wow(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("delete from wow where usuario_idusuario = '" + str(self.id_usuario) + "'"
                           " and post_idpost '" + str(id_post) + "')")
            return 1

        def dar_lol(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("insert into lol values ('" + str(self.id_usuario) + "' , '" + str(id_post) + "')")
            return 1

        def sacar_lol(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("delete from lol where usuario_idusuario = '" + str(self.id_usuario) + "'"
                           " and post_idpost '" + str(id_post) + "')")
            return 1

        def dar_beautiful(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("insert into beautiful values ('" + str(self.id_usuario) + "' , '" + str(id_post) + "')")
            return 1

        def sacar_beautiful(self, id_post, db):
            cursor = db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("delete from beautiful where usuario_idusuario = '" + str(self.id_usuario) + "'"
                           " and post_idpost '" + str(id_post) + "')")
            return 1

        def cambiar_contrasena(self , nueva_contrasena , db):
            cursor = db.cursor(pymysql.cursors.DictCursor)
            if (len(nueva_contrasena) < 8):
                return 0

            cursor.execute("update usuario set contrasena_hash = '" + str(self.hashear_contrasena(nueva_contrasena)) + "'"
                           " where idusuario = '" + str(self.id_usuario) + "'")
            return 1