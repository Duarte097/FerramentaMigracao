create database bd_patrimonio;
use bd_patrimonio;
create table tb_endereco (
	end_codigo int not null primary key,
    end_descricao varchar(60)
);

insert into tb_endereco values (1, 'Rua São Paulo'),
							   (2, 'Rua das Flores'),
							    (3, 'Avenida Brasil');
create table tb_bairro (
	bai_codigo int not null primary key,
    bai_descricao varchar(60)
);

insert into tb_bairro values (1, 'São Luiz'),
							  (2, 'Centro'),
                              (3, 'Nazaré');
                              
create table tb_cidade (
	cid_codigo int not null primary key,
    cid_descricao varchar(60),
    cid_uf char(2)
);

insert into tb_cidade values (1, 'Santa Helena', 'PR'),
							  (2, 'Missal', 'PR'),
                              (3, 'São Paulo', 'SP');
                              
create table tb_departamento (
	dep_codigo int not null primary key,
    dep_descricao varchar(60)
);

insert into tb_departamento values (1, 'Informática'),
									(2, 'Financeiro'),
                                    (3, 'Recursos Humanos');
                                    
create table tb_marca (
	mar_codigo int not null primary key,
    mar_descricao varchar(60)
);

insert into tb_marca values (1, 'Samsung'), (2, 'Tramontina'),
				(3, 'philips');
                
create table tb_categoria (
	cat_codigo int not null primary key,
    cat_descricao varchar(60)
);

insert into tb_categoria values (1, 'Consumo'), (2, 'Eletronicos'),
	  (3, 'Ferramentas');
      
create table tb_predio (
	pre_codigo int not null primary key,
    pre_descricao varchar(60),
    pre_numero varchar(10),
    pre_endereco_end_codigo int
		references tb_endereco (end_codigo),
	pre_bairro_bai_codigo int
		references tb_bairro (bai_codigo),
	pre_cidade_cid_codigo int
		references tb_cidade (cid_codigo)
);

insert into tb_predio values (1, 'Edificio das Flores',
	'2312', 1, 1, 1), (2, 'Edificio Central',
	'2835', 1, 2, 2), (3, 'Edificio das Margaridas',
	'6867', 2, 1, 1);
    
create table tb_patrimonio (
		pat_codigo int not null primary key,
        pat_descricao varchar(60),
        pat_dataquisicao date,
        pat_vlraquisicao decimal(10,2),
        pat_observacao varchar(100),
        pat_localizacao varchar(60),
        pat_departamento_dep_codigo int 
			references tb_departamento (dep_codigo),
		pat_marca_mar_codigo int
			references tb_marca (mar_codigo),
		pat_categoria_cat_codigo int
			references tb_categoria (cat_codigo),
		pat_predio_pre_codigo int
			references tb_predio (pre_codigo)
);

insert into tb_patrimonio values (1, 'notebook', '2009-10-02',
2500.00, 'teclado quebrado','sala coordenação', 1, 1, 1, 1), (2, 'chave', '2009-10-02',
59.00, 'ótimo estado', 'sala professores', 1, 2, 3, 1), (3, 'folha sulfite', '2009-10-02',
5.00, 'pacote', 'sala da coordenação', 1, 1, 3, 1); 