CREATE PROCEDURE [dbo].[DW_WEAVE_TICKETS_SP] AS
BEGIN
        
    
	IF OBJECT_ID('[DW_WEAVE_TICKETS_JSON_D]', 'U') IS NOT NULL
        DROP TABLE DW_WEAVE_TICKETS_JSON_D;
    
   
    SELECT * INTO DW_WEAVE_TICKETS_JSON_D
    FROM (
        SELECT BulkColumn
        FROM OPENROWSET (BULK 'C:\DO_NOT_DELETE\Weave\Data Files\Weav.json', SINGLE_CLOB) AS j
    ) AS a;
    
	drop table DW_WEAVE_TICKETS_D_bkp;
	select * into DW_WEAVE_TICKETS_D_bkp from DW_WEAVE_TICKETS_D;
	TRUNCATE TABLE DW_WEAVE_TICKETS_D;
    
    INSERT INTO DW_WEAVE_TICKETS_D (
        [ID],
        [Ticket No],
        [Service Category Name],
        [Service Name],
        [Description],
        [Created Date],
        [Requester Name],
        [Ticket Status],
        [Current Step Name],
        [Closed Date],
        [Is Delayed],
        [Refresh Date]
		
    )
    SELECT 
        [id],
        [ticketNo],
        [serviceCategoryName],
        [serviceName],
        [description],
        [createdDate],
        [requesterName],
        [ticketStatus],
        [currentStepName],
        [closedDate],
        [isDelayed],
        GETDATE() AS [Refresh Date]
    FROM DW_WEAVE_TICKETS_JSON_D
    CROSS APPLY OPENJSON(BulkColumn, '$.data')
    WITH (
        [id] INT '$.id',
        [ticketNo] NVARCHAR(50) '$.ticketNo',
        [serviceCategoryName] NVARCHAR(100) '$.serviceCategoryName',
        [serviceName] NVARCHAR(100) '$.serviceName',
        [description] NVARCHAR(MAX) '$.description',
        [createdDate] DATETIME '$.createdDate',
        [requesterName] NVARCHAR(100) '$.requesterName',
        [ticketStatus] NVARCHAR(50) '$.ticketStatus',
        [currentStepName] NVARCHAR(50) '$.currentStepName',
        [closedDate] DATETIME '$.closedDate',
        [isDelayed] BIT '$.isDelayed',
		
    );
END;

select * from DW_WEAVE_TICKETS_D_bkp

