from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(movie=movie, user=request.user).first()
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['user_review'] = user_review
    template_data['average_rating'] = movie.average_rating()
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST':
        movie = Movie.objects.get(id=id)
        if Review.objects.filter(movie=movie, user=request.user).exists():
            return redirect('movies.show', id=id)
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')
        if rating:
            review = Review()
            review.rating = int(rating)
            review.comment = comment
            review.movie = movie
            review.user = request.user
            review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        template_data['movie_id'] = id
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        if rating:
            review.rating = int(rating)
            review.comment = comment
            review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect('movies.show', id=id)