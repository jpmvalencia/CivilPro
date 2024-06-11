CREATE TABLE constructora (
    nombre_con     VARCHAR2(100) NOT NULL,
    nit_con        VARCHAR2(30) NOT NULL,
    correo_con     VARCHAR2(50) NOT NULL,
    contraseña_con VARCHAR2(20) NOT NULL,
    telefono       NUMBER(15),
);

ALTER TABLE constructora ADD CONSTRAINT constructora_pk PRIMARY KEY ( nit_con );


CREATE TABLE miembro_proyecto (
    usuario_documento_usu         VARCHAR2(20) NOT NULL,
    proyecto_id_pro               VARCHAR2(20) NOT NULL,
    rol_nombre_rol                VARCHAR2(50) NOT NULL,
    proyecto_constructora_nit_con VARCHAR2(30) NOT NULL
);

ALTER TABLE miembro_proyecto ADD CONSTRAINT miembro_proyecto_pk PRIMARY KEY ( usuario_documento_usu,
                                                                              proyecto_id_pro );


CREATE TABLE proyecto (
    id_pro               VARCHAR2(20) NOT NULL,
    nombre_pro           VARCHAR2(100) NOT NULL,
    descripcion_pro      VARCHAR2(300),
    fecha_inicio_pro     DATE NOT NULL,
    fecha_final_pro      DATE,
    presupuesto          NUMBER(15),
    constructora_nit_con VARCHAR2(30) NOT NULL
);

ALTER TABLE proyecto ADD CONSTRAINT proyecto_pk PRIMARY KEY ( id_pro,
                                                              constructora_nit_con );

CREATE TABLE rol (
    nombre_rol VARCHAR2(50) NOT NULL
);

ALTER TABLE rol ADD CONSTRAINT rol_pk PRIMARY KEY ( nombre_rol );

CREATE TABLE tarea (
    id_tar           VARCHAR2(20) NOT NULL,
    nombre_tar       VARCHAR2(100) NOT NULL,
    descripcion_tar  VARCHAR2(300),
    fecha_inicio_tar DATE NOT NULL,
    fecha_final_tar  DATE,
    presupuesto      NUMBER(15),
    responsable      VARCHAR2(20) NOT NULL,
    id_pro           VARCHAR2(20) NOT NULL
);

ALTER TABLE tarea
    ADD CONSTRAINT tarea_pk PRIMARY KEY ( id_tar,
                                          responsable,
                                          id_pro );

CREATE TABLE usuario (
    nombre_usu     VARCHAR2(100) NOT NULL,
    apellido1_usu  VARCHAR2(100) NOT NULL,
    apellido2_usu  VARCHAR2(100) NOT NULL,
    documento_usu  VARCHAR2(20) NOT NULL,
    telefono_usu   NUMBER(15),
    correro_usu    VARCHAR2(100) NOT NULL,
    contraseña_usu VARCHAR2(100) NOT NULL,
);

ALTER TABLE usuario ADD CONSTRAINT usuario_pk PRIMARY KEY ( documento_usu );

ALTER TABLE constructora
    ADD CONSTRAINT constructora_pais_fk FOREIGN KEY ( pais_codigo_pa )
        REFERENCES pais ( codigo_pa );


ALTER TABLE miembro_proyecto
    ADD CONSTRAINT miembro_proyecto_proyecto_fk FOREIGN KEY ( proyecto_id_pro,
                                                              proyecto_constructora_nit_con )
        REFERENCES proyecto ( id_pro,
                              constructora_nit_con );

ALTER TABLE miembro_proyecto
    ADD CONSTRAINT miembro_proyecto_rol_fk FOREIGN KEY ( rol_nombre_rol )
        REFERENCES rol ( nombre_rol );

ALTER TABLE miembro_proyecto
    ADD CONSTRAINT miembro_proyecto_usuario_fk FOREIGN KEY ( usuario_documento_usu )
        REFERENCES usuario ( documento_usu );

ALTER TABLE proyecto
    ADD CONSTRAINT proyecto_constructora_fk FOREIGN KEY ( constructora_nit_con )
        REFERENCES constructora ( nit_con );

ALTER TABLE tarea
    ADD CONSTRAINT tarea_miembro_proyecto_fk FOREIGN KEY ( responsable,
                                                           id_pro )
        REFERENCES miembro_proyecto ( usuario_documento_usu,
                                      proyecto_id_pro );

