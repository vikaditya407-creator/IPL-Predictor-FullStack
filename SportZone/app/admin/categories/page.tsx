import { useEffect, useState } from 'react';
import { supabase } from '../../../lib/supabase';
import AdminSidebar from '../../../components/admin/AdminSidebar';
import CategoryForm from '../../../components/admin/CategoryForm';

const CategoriesPage = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingCategory, setEditingCategory] = useState(null);

  useEffect(() => {
    const fetchCategories = async () => {
      const { data, error } = await supabase.from('categories').select('*');
      if (error) console.error('Error fetching categories:', error);
      else setCategories(data);
      setLoading(false);
    };

    fetchCategories();
  }, []);

  const handleEdit = (category) => {
    setEditingCategory(category);
  };

  const handleDelete = async (id) => {
    const { error } = await supabase.from('categories').delete().eq('id', id);
    if (error) console.error('Error deleting category:', error);
    else setCategories(categories.filter((category) => category.id !== id));
  };

  return (
    <div className="flex">
      <AdminSidebar />
      <div className="flex-1 p-4">
        <h1 className="text-2xl font-bold mb-4">Categories</h1>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div>
            <table className="min-w-full border-collapse border border-gray-200">
              <thead>
                <tr>
                  <th className="border border-gray-200 p-2">Name</th>
                  <th className="border border-gray-200 p-2">Slug</th>
                  <th className="border border-gray-200 p-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                {categories.map((category) => (
                  <tr key={category.id}>
                    <td className="border border-gray-200 p-2">{category.name}</td>
                    <td className="border border-gray-200 p-2">{category.slug}</td>
                    <td className="border border-gray-200 p-2">
                      <button onClick={() => handleEdit(category)} className="text-blue-500">Edit</button>
                      <button onClick={() => handleDelete(category.id)} className="text-red-500 ml-2">Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <CategoryForm category={editingCategory} setEditingCategory={setEditingCategory} setCategories={setCategories} />
          </div>
        )}
      </div>
    </div>
  );
};

export default CategoriesPage;