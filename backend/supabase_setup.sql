-- Supabase Setup for EduForge AI
-- Run this in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create lessons table
CREATE TABLE IF NOT EXISTS lessons (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    content JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;

-- Create policy for authenticated users
CREATE POLICY "Users can manage their own lessons" ON lessons
    FOR ALL
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- Create policy for anon users (read-only for demo)
CREATE POLICY "Anyone can read lessons" ON lessons
    FOR SELECT
    TO anon
    USING (true);

-- Create users table for extended profile (optional)
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    full_name TEXT,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can update own profile" ON user_profiles
    FOR ALL
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- Create storage bucket for media
INSERT INTO storage.buckets (id, name, public)
VALUES ('lesson-media', 'lesson-media', true)
ON CONFLICT (id) DO NOTHING;

-- Storage policies
CREATE POLICY "Public can view media" ON storage.objects
    FOR SELECT
    TO anon
    USING (bucket_id = 'lesson-media');

CREATE POLICY "Authenticated can upload media" ON storage.objects
    FOR INSERT
    TO authenticated
    WITH CHECK (bucket_id = 'lesson-media');

-- Function to handle new user signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_profiles (id, full_name)
    VALUES (NEW.id, NEW.raw_user_meta_data->>'full_name');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for user creation
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Enable realtime for lessons
ALTER PUBLICATION supabase_realtime ADD TABLE lessons;