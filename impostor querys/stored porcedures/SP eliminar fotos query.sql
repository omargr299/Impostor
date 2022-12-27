USE [Impostor]
GO

/****** Object:  StoredProcedure [dbo].[EliminarFotos]    Script Date: 04/12/2022 07:34:40 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[EliminarFotos]
	@alumnoID int
AS
BEGIN
	if exists(select distinct alumnoID from Fotos where alumnoID=@alumnoID)
		begin
			delete from Fotos where alumnoID=@alumnoID
		end
END
GO

