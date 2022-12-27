USE [Impostor]
GO

/****** Object:  StoredProcedure [dbo].[AgregarAlumnos]    Script Date: 04/12/2022 07:21:12 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE PROCEDURE [dbo].[AgregarAlumnos] 

	-- Add the parameters for the stored procedure here
	@nombre varchar(max),
	@carrera varchar(max),
	@semestre int
AS
BEGIN
	
	declare @id int;
	set @id = 0
	if ((select count(id) from Alumnos)>0)
		begin
			set @id = (select max(id) from Alumnos) + 1;
		end
	if not exists(select * from Alumnos where @id=id)
		if @carrera = 'IIA' or @carrera = 'LCD' or @carrera = 'ICA'
			if @semestre <= 10 and @semestre > 0
				begin 
					insert into Alumnos values(@id,@nombre,@carrera,@semestre)
				end
END
GO

