USE [Impostor]
GO

/****** Object:  StoredProcedure [dbo].[ObtenerNombres]    Script Date: 04/12/2022 07:35:11 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [dbo].[ObtenerNombres]
	
AS
BEGIN
	SELECT id,nombre FROM Alumnos
END
GO

