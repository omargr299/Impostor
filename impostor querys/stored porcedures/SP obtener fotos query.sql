USE [Impostor]
GO

/****** Object:  StoredProcedure [dbo].[ObtenerFotos]    Script Date: 04/12/2022 07:34:56 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [dbo].[ObtenerFotos]
	@alumnoID int
AS
BEGIN
	select alumnoID,foto from Fotos where alumnoID = @alumnoID
END
GO

