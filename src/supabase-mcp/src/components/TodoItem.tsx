import { useState } from 'react';
import {
  HStack,
  Box,
  Text,
  IconButton,
  Checkbox,
  useToast,
} from '@chakra-ui/react';
import { FaTrash } from 'react-icons/fa';
import { supabase } from '../lib/supabase';
import type { Todo } from '../lib/supabase';

interface TodoItemProps {
  todo: Todo;
  onUpdate: () => void;
}

export default function TodoItem({ todo, onUpdate }: TodoItemProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const toast = useToast();

  async function toggleComplete() {
    try {
      const { error } = await supabase
        .from('todos')
        .update({ is_complete: !todo.is_complete })
        .eq('id', todo.id);

      if (error) throw error;
      onUpdate();
    } catch (error) {
      console.error('Error updating todo:', error);
      toast({
        title: 'Error updating todo',
        status: 'error',
        duration: 2000,
      });
    }
  }

  async function deleteTodo() {
    try {
      setIsDeleting(true);
      const { error } = await supabase
        .from('todos')
        .delete()
        .eq('id', todo.id);

      if (error) throw error;
      onUpdate();
    } catch (error) {
      console.error('Error deleting todo:', error);
      toast({
        title: 'Error deleting todo',
        status: 'error',
        duration: 2000,
      });
    } finally {
      setIsDeleting(false);
    }
  }

  return (
    <HStack spacing={4} width="100%" bg="white" p={4} borderRadius="md" boxShadow="sm">
      <Checkbox
        isChecked={todo.is_complete}
        onChange={toggleComplete}
        size="lg"
      />
      <Box flex="1">
        <Text
          textDecoration={todo.is_complete ? 'line-through' : 'none'}
          color={todo.is_complete ? 'gray.500' : 'black'}
        >
          {todo.title}
        </Text>
        {todo.description && (
          <Text fontSize="sm" color="gray.500">
            {todo.description}
          </Text>
        )}
      </Box>
      <IconButton
        aria-label="Delete todo"
        icon={<FaTrash />}
        onClick={deleteTodo}
        isLoading={isDeleting}
        colorScheme="red"
        variant="ghost"
        size="sm"
      />
    </HStack>
  );
} 