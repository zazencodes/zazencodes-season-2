import { useState } from 'react';
import {
  VStack,
  HStack,
  Input,
  Button,
  Textarea,
  useToast,
} from '@chakra-ui/react';
import { supabase } from '../lib/supabase';
import { useAuth } from '../lib/AuthContext';

export default function AddTodo() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();
  const { user } = useAuth();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;

    setIsLoading(true);
    try {
      const { error } = await supabase.from('todos').insert([
        {
          title: title.trim(),
          description: description.trim() || null,
          user_id: user?.id
        },
      ]);

      if (error) throw error;

      setTitle('');
      setDescription('');
      toast({
        title: 'Todo added!',
        status: 'success',
        duration: 2000,
      });
    } catch (error) {
      console.error('Error adding todo:', error);
      toast({
        title: 'Error adding todo',
        status: 'error',
        duration: 2000,
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ width: '100%' }}>
      <VStack spacing={4} align="stretch">
        <Input
          placeholder="What needs to be done?"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          size="lg"
        />
        <Textarea
          placeholder="Add a description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          size="sm"
        />
        <HStack justify="flex-end">
          <Button
            type="submit"
            colorScheme="blue"
            isLoading={isLoading}
            loadingText="Adding..."
          >
            Add Todo
          </Button>
        </HStack>
      </VStack>
    </form>
  );
} 