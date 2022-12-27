USE [Impostor]
GO

/****** Object:  StoredProcedure [dbo].[EliminarAlumnos]    Script Date: 04/12/2022 07:32:47 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [dbo].[EliminarAlumnos]
	@ID int
AS
BEGIN
	if exists(select * from Alumnos where @id=id)
		begin
			delete from Alumnos where @id=id
			update Alumnos set id = id-1 where id>@ID
			update Dotos set idAlumno = idAlumno-1 where idAlumno>@ID
		end
END
GO

