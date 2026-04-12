-- EduForge AI - Supabase Database Setup
-- Run this in Supabase SQL Editor

-- Create lessons table
CREATE TABLE lessons (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  content_standard TEXT,
  content_simplified TEXT,
  content_accessibility TEXT,
  ui_hints TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;

-- Allow all operations (for demo - change in production)
CREATE POLICY "Allow all" ON lessons FOR ALL USING (true) WITH CHECK (true);

-- Create index for faster queries
CREATE INDEX idx_lessons_category ON lessons(category);
CREATE INDEX idx_lessons_created_at ON lessons(created_at DESC);

-- Verify table created
SELECT * FROM lessons LIMIT 0;
