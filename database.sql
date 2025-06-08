-- Drop tables if they exist to start from a clean slate
DROP TABLE IF EXISTS attendance, opportunities, trainings, consultant_skills, skills, resumes, consultants CASCADE;

-- Consultants Table
CREATE TABLE consultants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    department VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Resumes Table
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    consultant_id INTEGER NOT NULL REFERENCES consultants(id) ON DELETE CASCADE,
    file_path VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Pending' -- Pending, Updated
);

-- Skills Master Table
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Consultant Skills Link Table
CREATE TABLE consultant_skills (
    consultant_id INTEGER NOT NULL REFERENCES consultants(id) ON DELETE CASCADE,
    skill_id INTEGER NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (consultant_id, skill_id)
);

-- Trainings Table
CREATE TABLE trainings (
    id SERIAL PRIMARY KEY,
    consultant_id INTEGER NOT NULL REFERENCES consultants(id) ON DELETE CASCADE,
    course_name VARCHAR(255) NOT NULL,
    completed_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'Not Started', -- Not Started, In Progress, Completed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Opportunities Table
CREATE TABLE opportunities (
    id SERIAL PRIMARY KEY,
    consultant_id INTEGER NOT NULL REFERENCES consultants(id) ON DELETE CASCADE,
    opportunity_description TEXT,
    status VARCHAR(50) NOT NULL, -- Scheduled, Passed, Failed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Attendance Table
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    consultant_id INTEGER NOT NULL REFERENCES consultants(id) ON DELETE CASCADE,
    meeting_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL, -- Completed, Missed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert Dummy Data
INSERT INTO consultants (name, email, department) VALUES
('John Doe', 'john.doe@example.com', 'Technology'),
('Jane Smith', 'jane.smith@example.com', 'Business'),
('Peter Jones', 'peter.jones@example.com', 'Technology');

INSERT INTO skills (name) VALUES
('Python'),
('FastAPI'),
('SQLAlchemy'),
('PostgreSQL'),
('Docker'),
('React'),
('Project Management');

-- Assign some skills to consultants
INSERT INTO consultant_skills (consultant_id, skill_id) VALUES
(1, 1), -- John Doe -> Python
(1, 2), -- John Doe -> FastAPI
(1, 4), -- John Doe -> PostgreSQL
(2, 6), -- Jane Smith -> React
(2, 7); -- Jane Smith -> Project Management

-- Add some training records
INSERT INTO trainings (consultant_id, course_name, completed_date, status) VALUES
(1, 'Advanced Python', '2024-07-01', 'Completed'),
(2, 'Agile Methodologies', '2024-06-15', 'Completed'),
(3, 'Docker Fundamentals', '2024-07-20', 'In Progress');

-- Add some opportunities
INSERT INTO opportunities (consultant_id, opportunity_description, status) VALUES
(1, 'Backend Developer role at Acme Corp', 'Scheduled'),
(2, 'Project Manager at XYZ Inc.', 'Passed');

-- Add attendance records
INSERT INTO attendance (consultant_id, meeting_date, status) VALUES
(1, '2024-07-15', 'Completed'),
(2, '2024-07-15', 'Completed'),
(3, '2024-07-15', 'Missed');

-- Add a resume record for a consultant
INSERT INTO resumes (consultant_id, file_path, status) VALUES
(1, 'resumes/john_doe_resume.pdf', 'Updated');

-- Commit; -- Not needed in most SQL runners but good practice in scripts 