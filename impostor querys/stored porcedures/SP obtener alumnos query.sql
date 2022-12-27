USE [Impostor]
GO

/****** Object:  StoredProcedure [dbo].[ObtenerAlumnos]    Script Date: 04/12/2022 07:33:44 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[ObtenerAlumnos]

AS
BEGIN
	select * from Alumnos
END
GO

