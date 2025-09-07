-- SQL_Queries.sql
-- Campus Event Management Platform

-- 1) Event Popularity Report (registrations per event)
SELECT e.EventName, COUNT(r.StudentID) AS TotalRegistrations
FROM Events e
LEFT JOIN Registrations r ON e.EventID = r.EventID
GROUP BY e.EventName
ORDER BY TotalRegistrations DESC;

-- 2) Student Participation Report (events attended per student)
SELECT s.Name, COUNT(a.EventID) AS EventsAttended
FROM Students s
JOIN Attendance a ON s.StudentID = a.StudentID
WHERE a.Status = 'Present'
GROUP BY s.Name
ORDER BY EventsAttended DESC;

-- 3) Attendance Percentage per Event
SELECT e.EventName,
       ROUND(100.0 * SUM(CASE WHEN a.Status='Present' THEN 1 ELSE 0 END) / NULLIF(COUNT(a.EventID),0), 2) AS AttendancePercent
FROM Events e
LEFT JOIN Attendance a ON e.EventID = a.EventID
GROUP BY e.EventName
ORDER BY AttendancePercent DESC;

-- 4) Average Feedback Score per Event
SELECT e.EventName, ROUND(AVG(f.Rating),2) AS AvgRating
FROM Events e
JOIN Feedback f ON e.EventID = f.EventID
GROUP BY e.EventName
ORDER BY AvgRating DESC;

-- 5) Top 3 Active Students (by events attended)
SELECT s.Name, COUNT(a.EventID) AS EventsAttended
FROM Students s
JOIN Attendance a ON s.StudentID = a.StudentID AND a.Status='Present'
GROUP BY s.Name
ORDER BY EventsAttended DESC
LIMIT 3;

-- 6) Filter by Event Type (example: Workshop)
SELECT e.EventName, COUNT(r.StudentID) AS TotalRegistrations
FROM Events e
LEFT JOIN Registrations r ON e.EventID = r.EventID
WHERE e.EventType = 'Workshop'
GROUP BY e.EventName
ORDER BY TotalRegistrations DESC;
