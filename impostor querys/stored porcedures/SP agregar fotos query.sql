USE [Impostor]
GO

/****** Object:  StoredProcedure [dbo].[AgregarFotos]    Script Date: 04/12/2022 07:34:12 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [dbo].[AgregarFotos] 
	@alumnoID int,
	@foto varbinary(max)
AS
BEGIN
	if exists(select id from Alumnos where id=@alumnoID)
		begin
			declare @id int;
			set @id = 0
			if ((select count(id) from Fotos)>0)
				begin
					set @id = (select max(id) from Fotos) + 1;
				end
			insert into Fotos values(@id,@alumnoID,@foto)
		end
END
GO

