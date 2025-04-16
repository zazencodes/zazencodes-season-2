-- Create wallpapers table to store metadata
CREATE TABLE IF NOT EXISTS wallpapers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    style TEXT NOT NULL,
    color1 TEXT,
    color2 TEXT,
    color_mode TEXT,
    opacity INTEGER,
    blur INTEGER,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    prompt TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

-- Create index for faster queries by user_id
CREATE INDEX IF NOT EXISTS wallpapers_user_id_idx ON wallpapers(user_id);

-- Create index for sorting by creation date
CREATE INDEX IF NOT EXISTS wallpapers_created_at_idx ON wallpapers(created_at);

-- Enable Row Level Security
ALTER TABLE wallpapers ENABLE ROW LEVEL SECURITY;

-- Create policy to allow users to view only their own wallpapers
CREATE POLICY wallpapers_select_policy ON wallpapers
    FOR SELECT USING (auth.uid() = user_id);

-- Create policy to allow users to insert only their own wallpapers
CREATE POLICY wallpapers_insert_policy ON wallpapers
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create policy to allow users to update only their own wallpapers
CREATE POLICY wallpapers_update_policy ON wallpapers
    FOR UPDATE USING (auth.uid() = user_id);

-- Create policy to allow users to delete only their own wallpapers
CREATE POLICY wallpapers_delete_policy ON wallpapers
    FOR DELETE USING (auth.uid() = user_id);

-- Create storage bucket for wallpaper images
INSERT INTO storage.buckets (id, name, public) 
VALUES ('wallpapers', 'wallpapers', true)
ON CONFLICT (id) DO NOTHING;

-- Enable Row Level Security on storage bucket
UPDATE storage.buckets SET public = true WHERE id = 'wallpapers';

-- Create policy to allow users to select their own wallpaper images
CREATE POLICY wallpapers_storage_select_policy ON storage.objects
    FOR SELECT USING (
        bucket_id = 'wallpapers' AND 
        (storage.foldername(name))[1] = auth.uid()::text
    );

-- Create policy to allow users to insert their own wallpaper images
CREATE POLICY wallpapers_storage_insert_policy ON storage.objects
    FOR INSERT WITH CHECK (
        bucket_id = 'wallpapers' AND 
        (storage.foldername(name))[1] = auth.uid()::text
    );

-- Create policy to allow users to update their own wallpaper images
CREATE POLICY wallpapers_storage_update_policy ON storage.objects
    FOR UPDATE USING (
        bucket_id = 'wallpapers' AND 
        (storage.foldername(name))[1] = auth.uid()::text
    );

-- Create policy to allow users to delete their own wallpaper images
CREATE POLICY wallpapers_storage_delete_policy ON storage.objects
    FOR DELETE USING (
        bucket_id = 'wallpapers' AND 
        (storage.foldername(name))[1] = auth.uid()::text
    );

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update updated_at timestamp
CREATE TRIGGER update_wallpapers_updated_at
BEFORE UPDATE ON wallpapers
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
