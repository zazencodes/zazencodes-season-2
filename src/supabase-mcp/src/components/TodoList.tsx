import { useEffect, useState } from 'react';
import { VStack, Text, Spinner } from '@chakra-ui/react';
import { supabase } from '../lib/supabase';
import type { Todo } from '../lib/supabase';
import TodoItem from './TodoItem';
import { useAuth } from '../lib/AuthContext';

export default function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    fetchTodos();
  }, [user]);

  async function fetchTodos() {
    try {
      const { data, error } = await supabase
        .from('todos')
        .select('*')
        .eq('user_id', user?.id)
        .order('created_at', { ascending: false });

      if (error) throw error;
      setTodos(data || []);
    } catch (error) {
      console.error('Error fetching todos:', error);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <VStack>
        <Spinner size="xl" />
      </VStack>
    );
  }

  if (todos.length === 0) {
    return (
      <VStack>
        <Text>No todos yet! Add one above.</Text>
      </VStack>
    );
  }

  return (
    <VStack spacing={4} align="stretch" width="100%">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onUpdate={fetchTodos}
        />
      ))}
    </VStack>
  );
} 