

/*======================================================================================================================================================
CREATE  BY		– Ravi
TABLES USED		- DiscordHistory
USED IN FORM	- Discord
======================================================================================================================================================
SNO.  CHANGE BY			DATE			REASON
======================================================================================================================================================
======================================================================================================================================================
EXEC [DiscordBot_storedProcedure] 'I' ,'test1'
EXEC [DiscordBot_storedProcedure] 'S' ,''

======================================================================================================================================================*/
ALTER PROCEDURE [dbo].[DiscordBot_storedProcedure]
(
	/*1*/	@flag				char(1) = 'I',     -- I for insertion  and S for selection
	/*2*/	@Query			    VARCHAR(500)=''

	 
)
AS

IF(@flag='I')
Begin
	IF not EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES   WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME='DiscordHistory') 
		Begin
			create table DiscordHistory(
			 [pk_id] [int] IDENTITY(1,1) NOT NULL,

			   [Query] [varchar](200) NULL,
 
			   [CreationDate] [datetime] NULL
			 )
		End

		insert into DiscordHistory(Query,CreationDate)
		select @Query,getdate()
End

Else if(@flag='S')
Begin
	IF  EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES   WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME='DiscordHistory') 
		Begin
			select distinct Query Query,convert(datetime, CreationDate, 103) Cdate from DiscordHistory order by convert(datetime, CreationDate, 103) desc
		End
	else
	begin
		 
			create table DiscordHistory(
			 [pk_id] [int] IDENTITY(1,1) NOT NULL,

			   [Query] [varchar](200) NULL,
 
			   [CreationDate] [datetime] NULL
			 )
		select  Query,CreationDate from DiscordHistory
	end

End
select 11 'Query',22 'Query2'