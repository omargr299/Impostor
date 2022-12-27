USE [Impostor]
GO

/****** Object:  StoredProcedure [dbo].[CantidadFotos]    Script Date: 04/12/2022 07:34:27 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[CantidadFotos]
	@alumnoID int
AS
BEGIN
	select count(foto) from Fotos where alumnoID = @alumnoID
END
GO

